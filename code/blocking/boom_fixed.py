#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 Program: boom_fixed.py

 Date: 09/22/2021

 Author: Travis Phillips

 Purpose: An "OH NOES!!!" Program.  Now with 100% less "OH NOES!!!"
"""
import sys
import signal
from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QLabel, QPushButton)

class Boom(QWidget):
    """
    This class provides a simple UI to show why you don't
    block on the UI thread.
    """
    def __init__(self):
        """ Initalize the class. """
        super(Boom).__init__()
        self._init_win()

    def _init_win(self):
        """ Initialize the window. """
        # Set the size and title bar.
        self.setWindowTitle('Boom')
        self.setGeometry(300, 300, 300, 400)

        # Add the VBox as the main layout
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        # Add a label for the counter.
        self.lbl_counter = QLabel("0")
        self.lbl_counter.setStyleSheet("QLabel{font-size: 100pt;}")
        self.lbl_counter.setAlignment(Qt.AlignCenter)
        self.vbox.addWidget(self.lbl_counter)

        # Add a button to go boom.
        self.btn_boom = QPushButton("Boom?")
        self.vbox.addWidget(self.btn_boom)

        # Add increment button
        self.btn_inc = QPushButton("Add one")
        self.vbox.addWidget(self.btn_inc)

        # Connect the button clicks to the callback functions.
        self.btn_boom.clicked.connect(self._cb_clicked_boom)
        self.btn_inc.clicked.connect(self._cb_clicked_inc)

        # The fix: use a QTimer instead of sleep().
        self.timer = QTimer()

        # Connect the QTimer to a timeout callback.
        self.timer.timeout.connect(self.cb_timeout)

        # Finally show the window.
        self.show()

    def _cb_clicked_boom(self):
        """ Don't use sleep, instead start the QTimer. """
        #sleep(10) # <== This is a blocking call and a poor life choice in a UI
        #self.lbl_counter.setText(str(int(self.lbl_counter.text()) + 10))
        if not self.timer.isActive():
            # Timer is in msecs, set for 10 seconds.
            self.timer.start(10000)

            # And might as well disable the button till the timeout comes.
            self.btn_boom.setEnabled(False)

    def _cb_clicked_inc(self):
        """ Add one to the label """
        self.lbl_counter.setText(str(int(self.lbl_counter.text()) + 1))

    def cb_timeout(self):
        """
        sleep() is for the weak. Take a timeout instead.

        This triggers when QTimer timeout occurs. This doesn't block the
        GUI thread.
        """
        self.lbl_counter.setText(str(int(self.lbl_counter.text()) + 10))
        # Don't forget to stop the timer or it will keep running.
        if self.timer.isActive():
            self.timer.stop()

            # And give the button back to the user.
            self.btn_boom.setEnabled(True)

def main():
    """ Main program logic """
    # Make it so we can exit with Ctrl+C from terminal.
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Standard QT boilerplate to launch our UI
    app = QApplication(sys.argv)

    # pylint: disable=unused-variable
    # Reason: Disable the unused-variable violations. The
    #         'gui' variable is required to start the UI instance.
    gui = Boom()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
