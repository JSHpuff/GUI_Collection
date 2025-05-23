#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 UART Terminal Logic Module
 ===========================
 - Implements the functionality for the UART HEX Terminal application.
 
 - Handles: 
        1. Serial communication
        2. Setting management
        3. User interaction

 - Features:
        1. Serial port connection and communication
        2. Hex data transmission and reception
        3. Settings persistence
        4. Configurable delays
        5. Continuous monitoring mode
        6. Threaded operations for non-blocking UI

 - Classes:
        * UARTTerminal: Main application class

"""

import os
import json
import serial
import serial.tools.list_ports
import time
import threading
from PyQt5.QtCore import pyqtSignal, QObject

from uart_terminal_ui import UARTTerminalUI


class CommunicationSignals(QObject):
    """Signals for thread-safe communication between worker threads and UI"""
    message_received = pyqtSignal(str)
    status_update = pyqtSignal(str, str)  # status text, color
    connection_complete = pyqtSignal(bool)  # success/failure


class UARTTerminal(UARTTerminalUI):
    def __init__(self):
        super().__init__()
        
        # Serial port object
        self.serial_port = None
        
        # Threading
        self.serial_thread = None
        self.stop_thread = threading.Event()
        
        # Signals for thread communication
        self.signals = CommunicationSignals()
        self.signals.message_received.connect(self.update_terminal)
        self.signals.status_update.connect(self.update_status)
        self.signals.connection_complete.connect(self.on_connection_complete)
        
        # Config file path
        self.config_path = os.path.join(os.path.expanduser("~"), "uart_config.json")
        self.settings = {
            "port": "",
            "baudrate": "115200"
        }
        
        # Load saved settings
        self.load_settings()
        
        # Connect signals
        self.refresh_button.clicked.connect(self.refresh_ports)
        self.save_button.clicked.connect(self.save_settings)
        self.clear_button.clicked.connect(self.clear_terminal)
        self.transmit_button.clicked.connect(self.send_and_disconnect_threaded)
        
        # Initialize the port list
        self.refresh_ports()
        
        # Set default baudrate from settings
        index = self.baud_combo.findText(self.settings["baudrate"])
        if index >= 0:
            self.baud_combo.setCurrentIndex(index)
    
    def refresh_ports(self):
        """Refresh the list of available serial ports"""
        current_port = self.port_combo.currentText()
        self.port_combo.clear()
        ports = [port.device for port in serial.tools.list_ports.comports()]
        if ports:
            self.port_combo.addItems(ports)
            # Restore previous selection if it exists
            if current_port in ports:
                index = self.port_combo.findText(current_port)
                self.port_combo.setCurrentIndex(index)
            elif self.settings["port"] in ports:
                index = self.port_combo.findText(self.settings["port"])
                self.port_combo.setCurrentIndex(index)
        else:
            self.port_combo.addItem("No ports available")
    
    def connect_to_device(self):
        """Establish a connection to the selected serial port"""
        try:
            port = self.port_combo.currentText()
            if port == "No ports available":
                self.signals.message_received.emit("<No valid port selected>\n")
                return False
            
            baudrate = int(self.baud_combo.currentText())
            
            self.serial_port = serial.Serial(
                port=port,
                baudrate=baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=0.1
            )

            # Update UI through signals
            self.signals.status_update.emit("Connected", "green")
            self.signals.message_received.emit(f"<Connected to {port} at {baudrate} baud>\n")
            return True
            
        except Exception as e:
            self.signals.message_received.emit(f"<Connection error: {str(e)}>\n")
            self.signals.status_update.emit("Connection Failed", "red")
            return False
    
    def disconnect_from_device(self):
        """Disconnect from the current serial port"""
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
            self.serial_port = None
            
        # Update UI through signals
        self.signals.status_update.emit("Disconnected", "red")
        self.signals.message_received.emit("<Disconnected from device>\n")
        self.signals.message_received.emit("=================================\n")
    
    def serial_worker(self, hex_input):
        """Worker function that runs in a separate thread"""
        # Step 1: Connect
        if not self.connect_to_device():
            self.signals.connection_complete.emit(False)
            return
            
        # Step 2: Send message
        try:
            # Remove any spaces and validate hex characters
            hex_input = ''.join(hex_input.split())
            
            # Check if input is valid hex
            try:
                byte_data = bytes.fromhex(hex_input)
            except ValueError:
                self.signals.message_received.emit("<Invalid hex format>\n")
                self.disconnect_from_device()
                self.signals.connection_complete.emit(False)
                return
                
            # Send the data
            self.serial_port.write(byte_data)
            
            # Display what was sent
            formatted_hex = ' '.join([hex_input[i:i+2] for i in range(0, len(hex_input), 2)]).upper()
            self.signals.message_received.emit(f"TX: {formatted_hex}\n")

            # Wait a bit for response
            # time.sleep(0.5)
            
            # Check for response with timeout
            timeout = time.time() + 2  # 2 second timeout
            received_data = bytearray()
            
            while time.time() < timeout:
                if self.stop_thread.is_set():
                    break
                    
                bytes_available = self.serial_port.in_waiting
                if bytes_available > 0:
                    data = self.serial_port.read(bytes_available)
                    received_data.extend(data)
                    # Continue reading for a bit more to catch complete response
                    time.sleep(0.1)
                else:
                    # If we already have some data and no more is coming, break
                    if received_data:
                        break
                    time.sleep(0.05)
            
            if received_data:
                hex_data = received_data.hex(' ').upper()
                self.signals.message_received.emit(f"RX: {hex_data}\n")
                # Also show ASCII representation if printable
                ascii_data = ''.join(chr(b) if 32 <= b < 127 else '.' for b in received_data)
                self.signals.message_received.emit(f"RX (ASCII): {ascii_data}\n")
            else:
                self.signals.message_received.emit("RX: <No response received>\n")
            
        except Exception as e:
            self.signals.message_received.emit(f"<Send error: {str(e)}>\n")
        
        # Step 3: Disconnect
        self.disconnect_from_device()
        self.signals.connection_complete.emit(True)
    
    def send_and_disconnect_threaded(self):
        """Connect, send message, and disconnect workflow using threading"""
        # Check if a thread is already running
        if self.serial_thread and self.serial_thread.is_alive():
            self.terminal_display.append("<Another operation is in progress>\n")
            return
        
        # Get hex input
        hex_input = self.transmit_input.text().strip()
        if not hex_input:
            self.terminal_display.append("<No data to send>\n")
            return
        
        # Disable send button during operation
        self.transmit_button.setEnabled(False)
        self.transmit_button.setText("Sending...")
        
        # Reset stop event
        self.stop_thread.clear()
        
        # Create and start thread
        self.serial_thread = threading.Thread(
            target=self.serial_worker,
            args=(hex_input,),
            daemon=True
        )
        self.serial_thread.start()
    
    def on_connection_complete(self, success):
        """Called when the threaded operation completes"""
        self.transmit_button.setEnabled(True)
        self.transmit_button.setText("Send Hex")
    
    def update_terminal(self, message):
        """Thread-safe method to update terminal display"""
        self.terminal_display.append(message)
    
    def update_status(self, status_text, color):
        """Thread-safe method to update status"""
        self.status_value.setText(status_text)
        self.status_value.setStyleSheet(f"color: {color};")
    
    def save_settings(self):
        """Save the current port and baudrate settings"""
        port = self.port_combo.currentText()
        if port != "No ports available":
            self.settings["port"] = port
        self.settings["baudrate"] = self.baud_combo.currentText()
        
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.settings, f)
            self.terminal_display.append("<Settings saved>\n")
        except Exception as e:
            self.terminal_display.append(f"<Error saving settings: {str(e)}>\n")
    
    def load_settings(self):
        """Load saved settings if they exist"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    loaded_settings = json.load(f)
                    self.settings.update(loaded_settings)
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    def clear_terminal(self):
        """Clear the terminal display"""
        self.terminal_display.clear()
    
    def closeEvent(self, event):
        """Handle window close event to properly clean up resources"""
        # Signal thread to stop
        self.stop_thread.set()
        
        # Wait for thread to finish
        if self.serial_thread and self.serial_thread.is_alive():
            self.serial_thread.join(timeout=1.0)
        
        # Close serial port
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        
        event.accept()