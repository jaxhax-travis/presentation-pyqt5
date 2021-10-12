#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 Program: keygen.py

 Date: 02/23/2021

 Author: Travis Phillips

 Purpose: A keygen that can accept a challenge string in as an argument
          and will generate and print out the correct key for that
          challenge string. This is intended to be an internal tool to
          allow us to check peoples answers on social media.
"""
import sys
import string
import signal
# pylint: disable=no-name-in-module
# Reason: Pylint can't find these Q* namespaces in the PyQT5 module.
#         They do exist.
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QHBoxLayout, QVBoxLayout,
                             QLineEdit, QPushButton)

class KeyGen:
    """
    A class that takes in a challenge and generates a key from it.
    The key will be generated once initalized with a challenge.
    The challenge is expected to be a 32 character hex string. The
    key that is generated can be pulled from the value 'final_key'.
    """
    def __init__(self, challenge):
        """ initalize and generate our key """
        self.challenge = challenge

        # Generate a lookup table of chars.
        self.index = string.ascii_uppercase + string.digits

        # Initalize an index to hold the key parts in.
        self.keys = []

        # Initalize indexes to hold chunks of the challenge string.
        self.part = []
        self.num = []

        # Check if the challenge string is valid.
        # if not this will throw an exception.
        self.is_challenge_valid()

        # Split string into working parts
        self.split_string_parts()
        self.get_number_parts()

        # Run the Key Generator.
        self.gen_key()

    def is_challenge_valid(self):
        """
        Validate that the challenge code is a
        32 character hex string
        """
        # Ensure it's a string...
        if not isinstance(self.challenge, str):
            raise ValueError('challenge value must be a string')

        # ...of 32 characters...
        if len(self.challenge) != 32:
            raise ValueError('challenge must be 32 characters long.')

        # ... All of them being hex letters...
        for idx, char in enumerate(self.challenge):
            if char not in string.hexdigits:
                msg = "Invalid character in challenge string.\n"
                msg += "at index {0:d}: got chr {1:s}".format(idx, char)
                raise ValueError(msg)

    def split_string_parts(self):
        """ Break the challenge string into 4 parts. """
        self.part.append(self.challenge[0:8])
        self.part.append(self.challenge[8:16])
        self.part.append(self.challenge[16:24])
        self.part.append(self.challenge[24:32])

    def get_number_parts(self):
        """ convert 4 parts into ints from their hex value. """
        self.num.append(int(self.part[0], 16))
        self.num.append(int(self.part[1], 16))
        self.num.append(int(self.part[2], 16))
        self.num.append(int(self.part[3], 16))

    def gen_key(self):
        """ Generates the parts of the full final key and combines them. """
        self.keys.append(self.gen_key1())
        self.keys.append(self.gen_key2())
        self.keys.append(self.gen_key3())
        self.keys.append(self.gen_key4())
        self.keys.append(self.gen_key5())
        self.final_key = self.combine_keys()

    def gen_key1(self):
        """ Generate the 1st chunk of the final key. """
        key = self.lookup(self.num[0] ^ self.num[1])
        key += self.lookup(self.num[0] ^ self.num[2])
        key += self.lookup(self.num[0] ^ self.num[3])
        key += self.lookup(self.num[3] ^ self.num[1])
        key += self.lookup(self.num[3] ^ self.num[2])
        return key

    def gen_key2(self):
        """ Generate the 2nd chunk of the final key. """
        key = self.lookup(self.num[2] ^ self.num[1])
        key += self.lookup((self.num[0] ^ self.num[1]) + (self.num[0] ^ self.num[1]))
        key += self.lookup((self.num[1] ^ self.num[2]) + (self.num[0] ^ self.num[3]))
        key += self.lookup((self.num[1] ^ self.num[0]) + self.num[0])
        key += self.lookup((self.num[0] ^ self.num[2]) + self.num[2])
        return key

    def gen_key3(self):
        """ Generate the 3rd chunk of the final key. """
        key = self.lookup(self.num[2] % self.num[1])
        key += self.lookup(self.num[0] % self.num[3])
        key += self.lookup((self.num[0] % self.num[2]) + 42)
        key += self.lookup(self.num[3] + self.num[1])
        key += self.lookup(self.num[1] % self.num[3])
        return key

    def gen_key4(self):
        """ Generate the 4th chunk of the final key. """
        key = self.part[0][3].upper()
        key += self.part[1][1].upper()
        key += self.part[2][3].upper()
        key += self.part[3][3].upper()
        key += self.part[3][7].upper()
        return key

    def gen_key5(self):
        """ Generate the 5th chunk of the final key. """
        key = self.part[0][7].upper()
        key += self.part[1][3].upper()
        key += self.part[1][3].upper()
        key += self.part[2][1].upper()
        key += self.part[3][3].upper()
        return key[::-1]

    def combine_keys(self):
        """ Combine the key parts into the final key. """
        final_key = ""
        for key in self.keys:
            final_key += key
            final_key += "-"
        final_key = final_key[:-1]
        return final_key

    def lookup(self, val):
        """
        Attempt a wrap-around lookup of a number value
        against a character lookup table.
        """
        return self.index[val % len(self.index)]

class KeyGenUI(QWidget):
    """
    This class provides a simple UI for the keygen.
    """
    def __init__(self):
        """ Initalize the UI. """
        super().__init__()
        self.init_win()

    def cb_btn_gen_clicked(self):
        """
        Generate Key button callback function. Will create a KeyGen
        Instance and populate the Key textbox with the key.
        """
        try:
            keygen = KeyGen(self.txt_chall.text())
            self.txt_key.setText(keygen.final_key)
        except ValueError as err:
            self.txt_key.setText("Error: {0:s}".format(str(err)))

    def init_win(self):
        """ Populate the widgets and show the window. """
        # Set the size and title bar.
        self.setWindowTitle('March 2021 Challenge KeyGenMe Generator')
        self.setGeometry(300, 300, 425, 125)

        # Create the main VBox Layout container
        vbox = QVBoxLayout()

        # Create a HBox for the Challenge Code section of the form.
        hbox = QHBoxLayout()

        # Create a line entry for the user to enter the challenge code
        # and attach it to the HBox
        self.txt_chall = QLineEdit()
        self.txt_chall.setPlaceholderText("Challenge Code")
        self.txt_chall.returnPressed.connect(self.cb_btn_gen_clicked)
        hbox.addWidget(self.txt_chall)

        # Create a Generate Key button and attach it to the HBOX.
        self.btn_gen = QPushButton("Generate Key")
        self.btn_gen.clicked.connect(self.cb_btn_gen_clicked)
        hbox.addWidget(self.btn_gen)

        # Add the HBox to the main VBox Layout.
        vbox.addLayout(hbox)

        # Create a HBox for the Key Code section of the form.
        hbox = QHBoxLayout()

        # Create a line entry to display the key code to the user
        # when they generate it and attach it to the HBox
        self.txt_key = QLineEdit()
        self.txt_key.setPlaceholderText("Key Code")
        self.txt_key.setReadOnly(True)
        hbox.addWidget(self.txt_key)

        # Add the HBox to the main VBox Layout.
        vbox.addLayout(hbox)

        # Set the VBox as the window layout and show the window.
        self.setLayout(vbox)
        self.show()

def main():
    """ Main Application Logic. """
    if len(sys.argv) == 1:
        # Assume the User wants to run in GUI mode.
        print(" [*] Starting GUI...")
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        app = QApplication(sys.argv)
        # pylint: disable=unused-variable
        # Reason: Disable the unused-variable violations. The
        #         'gui' variable is required to start the UI instance.
        gui = KeyGenUI()
        sys.exit(app.exec_())
    elif sys.argv[1] in ("-h", "-H", "--help"):
        print("\n [*] Usage: {0:s} [CHALLENGE STRING]".format(sys.argv[0]))
        print(" [*] Example: {0:s} 0cbc6611f5540bd0809a388dc95a615b".format(sys.argv[0]))
        print("")
        return 1

    keygen = KeyGen(sys.argv[1])
    print(" [*] Challenge: {0:s}".format(keygen.challenge))
    print(" [*]  Key Code: {0:s}".format(keygen.final_key))
    return 0

if __name__ == "__main__":
    sys.exit(main())
