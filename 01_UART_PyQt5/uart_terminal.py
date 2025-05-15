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

 - Classes:
        * UARTTerminal: Main application class

"""

import os
import json
import serial
import serial.tools.list_ports
from uart_terminal_ui import UARTTerminalUI


class UARTTerminal(UARTTerminalUI):
    def __init__(self):
        super().__init__()
        
        # Serial port object
        self.serial_port = None
        
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
        self.transmit_button.clicked.connect(self.send_and_disconnect)
        
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
                self.terminal_display.append("<No valid port selected>\n")
                return False
            
            baudrate = int(self.baud_combo.currentText())
            
            self.serial_port = serial.Serial(
                port=port,
                baudrate=baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1
            )
            
            # Update UI
            self.status_value.setText("Connected")
            self.status_value.setStyleSheet("color: green;")
            self.terminal_display.append(f"<Connected to {port} at {baudrate} baud>\n")
            return True
            
        except Exception as e:
            self.terminal_display.append(f"<Connection error: {str(e)}>\n")
            self.status_value.setText("Connection Failed")
            self.status_value.setStyleSheet("color: red;")
            return False
    
    def disconnect_from_device(self):
        """Disconnect from the current serial port"""
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
            self.serial_port = None
            
        # Update UI
        self.status_value.setText("Disconnected")
        self.status_value.setStyleSheet("color: red;")
        self.terminal_display.append("<Disconnected from device>\n")
    
    def send_and_disconnect(self):
        """Connect, send message, and disconnect workflow"""
        # Step 1: Connect
        if not self.connect_to_device():
            return
            
        # Step 2: Send message
        try:
            # Get and parse hex input
            hex_input = self.transmit_input.text().strip()
            
            # Remove any spaces and validate hex characters
            hex_input = ''.join(hex_input.split())
            
            # Check if input is valid hex
            try:
                byte_data = bytes.fromhex(hex_input)
            except ValueError:
                self.terminal_display.append("<Invalid hex format>\n")
                self.disconnect_from_device()
                return
                
            # Send the data
            self.serial_port.write(byte_data)
            
            # Display what was sent
            formatted_hex = ' '.join([hex_input[i:i+2] for i in range(0, len(hex_input), 2)]).upper()
            self.terminal_display.append(f"TX: {formatted_hex}\n")
            
            # Check for response
            if self.serial_port.in_waiting > 0:
                data = self.serial_port.read(self.serial_port.in_waiting)
                hex_data = data.hex(' ').upper()
                self.terminal_display.append(f"RX: {hex_data}\n")
            
        except Exception as e:
            self.terminal_display.append(f"<Send error: {str(e)}>\n")
        
        # Step 3: Disconnect
        self.disconnect_from_device()
    
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
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        event.accept()