#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 Program: stopwatch_v1.py

 Date: 09/22/2021

 Author: Travis Phillips

 Purpose: A simple Stopwatch program.
"""
import sys
import signal
from PyQt5.QtCore import (Qt, QDateTime, QTime, QTimer)
from PyQt5.QtWidgets import (QApplication, QWidget, QHBoxLayout,
                             QLabel, QPushButton)

class Stopwatch(QWidget):
    """ This class provides a simple stopwatch widget. """
    start_time = None

    def __init__(self):
        """ Class Initalizer function. """
        super().__init__()
        # Set the size and title bar.
        self.setWindowTitle('Scoreboard')
        self.setGeometry(300, 300, 500, 150)

        # Add the Layout
        hbox = QHBoxLayout()
        self.setLayout(hbox)

        # Create a QLabel for displaying time duration
        self.lbl_time = QLabel("00:00:00.00")
        self.lbl_time.setStyleSheet("QLabel{font-size: 50pt;}")
        self.lbl_time.setAlignment(Qt.AlignCenter)

        # Create a Stop and Reset button
        self.btn_start = QPushButton("Start")
        btn_reset = QPushButton("Reset")

        # Add styles to the Stop and Reset button
        self.btn_start.setStyleSheet("QPushButton{font-size: 50pt;}")
        btn_reset.setStyleSheet("QPushButton{font-size: 50pt; background-color: red}")

        # Connect the buttons callbacks
        self.btn_start.clicked.connect(self._cb_start_stop)
        btn_reset.clicked.connect(self._cb_reset)

        # Pack the widgets into the layout
        hbox.addWidget(btn_reset)
        hbox.addWidget(self.lbl_time, 1)
        hbox.addWidget(self.btn_start)

        # Create a QTimer and attach it's timeout to the update time
        # callback. Note that we are not starting it yet.
        self.timer = QTimer()
        self.timer.timeout.connect(self._cb_update_time)

        # Finally show the window.
        self.show()

    def _cb_update_time(self):
        """ A function to update the label with the current time of run. """
        current_time = QDateTime.currentDateTime()
        diff = QTime(0, 0).addMSecs(self.start_time.msecsTo(current_time))
        duration = f"{diff.hour():02d}:"
        duration += f"{diff.minute():02d}:"
        duration += f"{diff.second():02d}."
        duration += f"{int(diff.msec() / 10):02d}"
        self.lbl_time.setText(duration)

    def _cb_start_stop(self):
        """ Start/pause the stopwatch. """
        if self.start_time is None:
            self.start_time = QDateTime.currentDateTime()
            self.lbl_time.setText("00:00:00.00")
            self.timer.start(10)
            self.btn_start.setText("Pause")
        elif self.btn_start.text().replace("&", "") == "Resume":
            self.timer.start(10)
            self.btn_start.setText("Pause")
        else:
            self.btn_start.setText("Resume")
            self.timer.stop()
            self._cb_update_time()

    def _cb_reset(self):
        """ Reset the timer. """
        if self.btn_start.text().replace("&", "") in ["Resume", "Start"]:
            self.btn_start.setText("Start")
            self.start_time = None
            self.lbl_time.setText("00:00:00.00")
        else:
            self.start_time = QDateTime.currentDateTime()

def main():
    """ Main program logic """
    # Make it so we can exit with Ctrl+C from terminal.
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Standard QT boilerplate to launch our UI
    app = QApplication(sys.argv)

    # pylint: disable=unused-variable
    # Reason: Disable the unused-variable violations. The
    #         'gui' variable is required to start the UI instance.
    gui = Stopwatch()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
