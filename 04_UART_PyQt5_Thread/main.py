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

# Below hack sometimes required when operating on windows git-bash/msys2
sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")

if __name__ == "__main__":
    # Creating a Qt Application
    """ 
        == QApplicaiton ==
        * Part of PyQt
        * Used to create GUI applications
        == sys.argv ==
        * Allows the app to handle command-line arguments
    """
    app = QApplication(sys.argv)

    # Initializing the main window
    window = UARTTerminal()
    window.show()

    # Running the application
    """
        == app.exec_() ==
        * Starts the Qt event loop
        * Waiting for user interactions
        == sys.exit() ==
        * Ensures the application exits cleanly when closed
    """
    sys.exit(app.exec_())