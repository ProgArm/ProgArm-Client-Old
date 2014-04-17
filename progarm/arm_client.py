# Copyright (C) 2014  Alex-Daniel Jakimenko <alex.jakimenko@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import serial
import time
import os
from datetime import datetime
from serial import SerialException


class ArmClient(object):
    def __init__(self, device):
        self.serial = None
        self.device = device
        self.actionDict = {}
        self.letters = []

    def init(self, baudrate=9600):
        self.letters = []
        self.serial = serial.Serial(self.device, baudrate)

    # def morseConvert(morseString):
    #    morseNumber=0
    #    morseMultiplier=1
    #
    #    for curChar in morseString:
    #        if curChar == '.':
    #            morseNumber += morseMultiplier
    #        else:
    #            morseNumber += morseMultiplier * 2
    #        morseMultiplier *= 2
    #
    #    return morseNumber - 1 # to start from 0 instead of 1

    def addAction(self, code, action):
        """
        code -- int value representing some morse code letter(s)
        action -- function pointer or string to be executed in a shell"""
#        numbers = []
#        for curChar in name:
#            charInt = getattr(morse_codes, "MORSE_" + curChar)
#            numbers.append(str(charInt))

        if isinstance(action, str):
            self.actionDict[code] = lambda: os.system(action)
        else:
            self.actionDict[code] = action

    def update(self):
        """This method should be called periodically"""
        self.processData(self.serial.read())

    def processData(self, command):
        """Actual data processing. Normally only one byte is processed,
        but sometimes this method might fetch additonal data.

        command -- single byte indicating command"""
        if command == "L":  # letter received
            actionKey = ord(self.serial.read())
            if actionKey in self.actionDict:
                action = self.actionDict[actionKey]
                action()
            else:
                self.actionNotFound(actionKey)
        elif command == "Q":  # forget everything, previous data is wrong
            # DEPRECATED
            self.letters = []
        elif command == "W":  # a whole word received
            # DEPRECATED
            pass
        elif command == "P":
            self.pongReceived()
        elif command == "p":
            self.pong()
        elif command == "d":
            self.sendDate()
        else:
            self.commandNotFound(command)

    def start(self):
        """Main loop. This method will never return"""
        online = False
        while True:  # loop for reconnection
            try:
                self.init()
                while True:  # loop for data reading
                    self.update()
                    if not online:
                        online = True
                        self.onConnect()
            except SerialException:
                if online:  # do not repeat fail error
                    online = False
                    print datetime.now()  # log current date
                    print "Unable to use serial interface! Restarting..."
                    self.onDisconnect()
                time.sleep(1)

    def ping(self):
        self.serial.write("p")

    def pong(self):
        self.serial.write("P")

    def pongReceived(self):
        print "Pong received"

    def sendDate(self):  # EXPERIMENTAL
        """Infrorm the device about the current date."""
        today = datetime.today()
        self.serial.write("D")
        self.serial.write(chr(int(str(today.year)[:2])))
        self.serial.write(chr(int(str(today.year)[2:])))
        self.serial.write(chr(today.month))
        self.serial.write(chr(today.day))
        self.serial.write(chr(today.hour))
        self.serial.write(chr(today.minute))
        self.serial.write(chr(today.second))

    def close(self):
        self.serial.close()

    def onConnect(self):
        pass

    def onDisconnect(self):
        pass

    def commandNotFound(self, command):
        print 'Error: Unknown command', command

    def actionNotFound(self, action):
        print 'Error: Unknown action', action
