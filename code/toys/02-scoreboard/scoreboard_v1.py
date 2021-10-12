#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 Program: scoreboard_v1.py

 Date: 09/22/2021

 Author: Travis Phillips

 Purpose: A simple scoreboard program.
"""
import sys
import signal
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QPushButton,
                             QSizePolicy)

class _ScoreboardCounter(QWidget):
    """
    This class provides a simple score counter widget that
    is self contained.
    """
    def __init__(self, parent):
        """ Initalize the class. """
        super(_ScoreboardCounter, self).__init__(parent)
        self._init_counter()

    def _init_counter(self):
        """ Initialize the counter. """
        # Create a VBox for the layout.
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        # Create the increment decrement buttons.
        btn_inc = QPushButton("+")
        btn_dec = QPushButton("-")

        # Apply stylesheets to the buttons
        btn_inc.setStyleSheet("QPushButton{font-size: 75pt; background-color: green}")
        btn_dec.setStyleSheet("QPushButton{font-size: 75pt; background-color: red}")
        btn_inc.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn_dec.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Create the scorekeeper label
        self.score = QLabel("0")

        # Apply stylesheets to the label
        self.score.setStyleSheet("QLabel{font-size: 100pt;}")
        self.score.setAlignment(Qt.AlignCenter)

        # Connect the button to the callback functions
        btn_inc.clicked.connect(self._cb_btn_inc_clicked)
        btn_dec.clicked.connect(self._cb_btn_dec_clicked)

        # Pack the widgets in the vbox
        vbox.addWidget(btn_inc, 1)
        vbox.addWidget(self.score, 3)
        vbox.addWidget(btn_dec, 1)

    def _cb_btn_inc_clicked(self):
        """ Callback function to increment the score. """
        self.score.setText(str(int(self.score.text()) + 1))

    def _cb_btn_dec_clicked(self):
        """ Callback function to decrement the score. """
        self.score.setText(str(int(self.score.text()) - 1))

class Scoreboard(QWidget):
    """
    This class provides a simple UI for the Scoreboard.
    """
    def __init__(self):
        """ Initalize the class. """
        super().__init__()
        self._init_win()

    def _init_win(self):
        """ Initialize the window. """
        # Set the size and title bar.
        self.setWindowTitle('Scoreboard')
        self.setGeometry(300, 300, 600, 400)

        # Add the HBox as the main layout
        self.hbox = QHBoxLayout()
        self.setLayout(self.hbox)

        # Create the counter widget.
        home = _ScoreboardCounter(self)
        away = _ScoreboardCounter(self)

        # Pack the widgets into the HBox. We use stretch factors here
        # to add some margins
        self.hbox.addStretch(1)
        self.hbox.addWidget(home, 3)
        self.hbox.addStretch(1)
        self.hbox.addWidget(away, 3)
        self.hbox.addStretch(1)

        # Finally show the window.
        self.show()

def main():
    """ Main program logic """
    # Make it so we can exit with Ctrl+C from terminal.
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Standard QT boilerplate to launch our UI
    app = QApplication(sys.argv)

    # pylint: disable=unused-variable
    # Reason: Disable the unused-variable violations. The
    #         'gui' variable is required to start the UI instance.
    gui = Scoreboard()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
