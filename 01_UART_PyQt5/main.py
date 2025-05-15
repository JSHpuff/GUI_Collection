#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 UART HEX Terminal Application
 ==============================

 - Main entry point for the UART HEX Terminal Application.

 - Initializes the PyQt application.

 - Launches the main window.
 
"""

import sys
from PyQt5.QtWidgets import QApplication
from uart_terminal import UARTTerminal

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UARTTerminal()
    window.show()
    sys.exit(app.exec_())