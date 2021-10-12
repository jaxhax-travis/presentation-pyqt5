#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 Program: all_in_one_v1.py

 Date: 09/22/2021

 Author: Travis Phillips

 Purpose: A All-in-One of our toy programs.
"""
import sys
import signal
from PyQt5.QtCore import (Qt, QDateTime, QTime, QTimer, QRandomGenerator)
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QPushButton,
                             QSizePolicy, QGroupBox, QComboBox)

class Dice(QGroupBox):
    """
    This class provides a simple UI for the Dice Roller.
    """
    # Storage of the dice we will support rolling.
    # Format: "Dice_name": [ranges for random numbers]
    DICE = {"D4": [1, 5],
            "D6": [1, 7],
            "D8": [1, 9],
            "D10A (0-9)": [0, 9],
            "D10B (00-90)": [0, 100], # Special handling for this one.
            "D12": [1, 13],
            "D20": [1, 21],
            "D100": [1, 101]}

    def __init__(self, parent):
        """ Initalize the class. """
        super(Dice, self).__init__("Dice Roller", parent)
        self.setStyleSheet("QGroupBox{font-size: 24pt;}")
        self._init_win()

    def _init_win(self):
        """ Initialize the window. """
        # Add the VBox as the main layout
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        # Add a combo box to select the dice type.
        self.combo_box = QComboBox(self)
        self.combo_box.setStyleSheet("QComboBox{font-size: 16pt;}")
        for dice_name in self.DICE:
            self.combo_box.addItem(dice_name)
        self.vbox.addWidget(self.combo_box)

        # Add a label for the roll value.
        self.lbl_dice = QLabel("0")
        self.lbl_dice.setStyleSheet("QLabel{font-size: 100pt;}")
        self.lbl_dice.setAlignment(Qt.AlignCenter)
        self.vbox.addWidget(self.lbl_dice)

        # Add a button to roll the dice.
        self.btn_roll = QPushButton("Roll Dice")
        self.btn_roll.setStyleSheet("QPushButton{font-size: 24pt; background-color: green}")
        self.vbox.addWidget(self.btn_roll)

        # Connect the button click to the roller function.
        self.btn_roll.clicked.connect(self._cb_clicked_roll)

        # Finally show the window.
        self.show()

    def _cb_clicked_roll(self):
        """ Handle the dice roll event. """
        # Get the user select dice type
        dice = self.combo_box.currentText()

        # Use QT's QRandomGenerator to give us a cryptographically
        # secure dice roller... becuase why not! XD
        roll = QRandomGenerator.securelySeeded().bounded(self.DICE[dice][0],
                                                         self.DICE[dice][1])

        # Handle the special D10B Dice
        if dice == "D10B (00-90)":
            self.lbl_dice.setText(f"{(roll % 10) * 10:02d}")
        else:
            self.lbl_dice.setText(f"{roll}")

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

class Scoreboard(QGroupBox):
    """
    This class provides a simple UI for the Scoreboard.
    """
    def __init__(self, parent):
        """ Initalize the class. """
        super(Scoreboard, self).__init__("Scoreboard", parent)
        self.setStyleSheet("QGroupBox{font-size: 24pt;}")
        self._init_win()

    def _init_win(self):
        """ Initialize the widget. """

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

class Stopwatch(QGroupBox):
    """ This class provides a simple stopwatch widget. """
    start_time = None

    def __init__(self, parent):
        """ Initalize the class. """
        super(Stopwatch, self).__init__("Stopwatch", parent)
        self.setStyleSheet("QGroupBox{font-size: 24pt;}")

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
            print("1")
            self.start_time = QDateTime.currentDateTime()
            self.lbl_time.setText("00:00:00.00")
            self.timer.start(10)
            self.btn_start.setText("Pause")
        elif self.btn_start.text().replace("&", "") == "Resume":
            print("2")
            self.timer.start(10)
            self.btn_start.setText("Pause")
        else:
            print("3")
            self.btn_start.setText("Resume")
            self.timer.stop()
            self._cb_update_time()

    def _cb_reset(self):
        """ Reset the timer. """
        print(self.btn_start.text())
        if self.btn_start.text().replace("&", "") in ["Resume", "Start"]:
            self.btn_start.setText("Start")
            self.start_time = None
            self.lbl_time.setText("00:00:00.00")
        else:
            self.start_time = QDateTime.currentDateTime()

class AllInOne(QWidget):
    """ All in One Toy UI """
    def __init__(self):
        """ Initalize the class. """
        super().__init__()
        self._init_win()

    def _init_win(self):
        # Set the size and title bar.
        self.setWindowTitle('All-In-One Game Night')
        self.setGeometry(300, 300, 1024, 600)

        # create layouts
        self.main_hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        self.setLayout(self.main_hbox)
        self.main_hbox.addLayout(vbox, 80)

        # Create instances of our toys.
        scoreboard = Scoreboard(self)
        stopwatch = Stopwatch(self)
        dice = Dice(self)

        # Pack the widgets into layouts.
        vbox.addWidget(stopwatch)
        vbox.addWidget(scoreboard)
        self.main_hbox.addWidget(dice, 20)

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
    gui = AllInOne()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
