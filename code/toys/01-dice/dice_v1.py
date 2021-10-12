#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 Program: dice_v1.py

 Date: 09/22/2021

 Author: Travis Phillips

 Purpose: A simple dice roller program.
"""
import sys
import signal
from PyQt5.QtCore import (Qt, QRandomGenerator)
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QComboBox, QLabel, QPushButton)

class Dice(QWidget):
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

    def __init__(self):
        """ Initalize the class. """
        super().__init__()
        self._init_win()

    def _init_win(self):
        """ Initialize the window. """
        # Set the size and title bar.
        self.setWindowTitle('Dice Roller')
        self.setGeometry(300, 300, 300, 400)

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

def main():
    """ Main program logic """
    # Make it so we can exit with Ctrl+C from terminal.
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Standard QT boilerplate to launch our UI
    app = QApplication(sys.argv)

    # pylint: disable=unused-variable
    # Reason: Disable the unused-variable violations. The
    #         'gui' variable is required to start the UI instance.
    gui = Dice()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
