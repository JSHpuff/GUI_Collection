#!/usr/bin/env python3
# -*- config: utf-8 -*-
"""
 UART Terminal UI Module
 ========================
 - Defines the user interface for the UART HEX Terminal application.
 
 - Contains the UI layout & components

 - Classes:
        * UARTTerminalUI: Main window UI class
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QComboBox, QPushButton, QLabel, 
                             QTextEdit, QLineEdit, QGridLayout, QGroupBox)


class UARTTerminalUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UART Hex Terminal")
        self.resize(600, 500)
        
        # Create main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Create UI components
        self.create_connection_group()
        self.create_terminal_group()
        self.create_transmit_group()
        
    def create_connection_group(self):
        connection_group = QGroupBox("Connection Settings")
        connection_layout = QGridLayout()
        
        # Port selection
        self.port_label = QLabel("Port:")
        self.port_combo = QComboBox()
        self.refresh_button = QPushButton("Refresh")
        
        # Baudrate selection
        self.baud_label = QLabel("Baudrate:")
        self.baud_combo = QComboBox()
        self.baud_combo.addItems(["9600", "19200", "38400", "57600", "115200", "230400", "460800", "921600"])
        
        # Save settings button
        self.save_button = QPushButton("Save Settings")
        
        # Status indicator
        self.status_label = QLabel("Status:")
        self.status_value = QLabel("Disconnected")
        self.status_value.setStyleSheet("color: red;")
        
        # Layout
        connection_layout.addWidget(self.port_label, 0, 0)
        connection_layout.addWidget(self.port_combo, 0, 1)
        connection_layout.addWidget(self.refresh_button, 0, 2)
        connection_layout.addWidget(self.baud_label, 1, 0)
        connection_layout.addWidget(self.baud_combo, 1, 1)
        connection_layout.addWidget(self.save_button, 1, 2)
        connection_layout.addWidget(self.status_label, 2, 0)
        connection_layout.addWidget(self.status_value, 2, 1, 1, 2)
        
        connection_group.setLayout(connection_layout)
        self.main_layout.addWidget(connection_group)
        
    def create_terminal_group(self):
        terminal_group = QGroupBox("Terminal")
        terminal_layout = QVBoxLayout()
        
        # Display area for received data
        self.terminal_display = QTextEdit()
        self.terminal_display.setReadOnly(True)
        self.terminal_display.setStyleSheet("font-family: monospace;")
        
        # Clear button
        self.clear_button = QPushButton("Clear Terminal")
        
        terminal_layout.addWidget(self.terminal_display)
        terminal_layout.addWidget(self.clear_button)
        
        terminal_group.setLayout(terminal_layout)
        self.main_layout.addWidget(terminal_group)
        
    def create_transmit_group(self):
        transmit_group = QGroupBox("Transmit")
        transmit_layout = QVBoxLayout()
        
        # Hex input field
        self.transmit_input = QLineEdit()
        self.transmit_input.setPlaceholderText("Enter hex data (e.g., FF 00 A3 BD)...")
        
        # Transmit button
        self.transmit_button = QPushButton("Send Hex")
        
        # Add to layout
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.transmit_input)
        input_layout.addWidget(self.transmit_button)
        
        transmit_layout.addLayout(input_layout)
        transmit_group.setLayout(transmit_layout)
        self.main_layout.addWidget(transmit_group)