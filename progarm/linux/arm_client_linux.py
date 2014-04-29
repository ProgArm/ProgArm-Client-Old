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

from ..arm_client import ArmClient
from progarm import input_codes
import os
import re
from os.path import dirname
# import abc


class ArmClientLinux(ArmClient):
    # __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(ArmClientLinux, self).__init__("/dev/rfcomm0")

        self.addAction(input_codes.INPUT_M, "amixer set Master toggle")

        self.addAction(input_codes.INPUT_N, dirname(__file__) + "/cmus_next &")
        self.addAction(input_codes.INPUT_P, "cmus-remote --prev &")
        self.addAction(input_codes.INPUT_C, dirname(__file__) + "/cmus_pause &")
        self.addAction(input_codes.INPUT_A, self.cmusToggleAaa)

        self.addAction(input_codes.INPUT_L, "amixer set Master playback 10%+ &")
        self.addAction(input_codes.INPUT_S, "amixer set Master playback 10%- &")

        self.addAction(input_codes.INPUT_T, dirname(__file__) + "/tell_time &")
        self.addAction(input_codes.INPUT_D, dirname(__file__) + "/tell_date &")

    def processData(self, command):
        if command == "V":  # EXPERIMENTAL
            ticks = ord(self.serial.read())
            if ticks > 127:  # negative numbers # TODO 127 ?
                self.volumeKnobDown(255 - ticks)
            else:
                self.volumeKnobUp(ticks)
        else:  # TODO remove else clause to allow further processing?
            return ArmClient.processData(self, command)

    def cmusToggleAaa(self):
        os.system("play -q -s -n synth tri %0 fade 0 1 1 &")
        os.system("cmus-remote -C 'toggle aaa_mode' &")

    # @abc.abstractmethod
    def volumeKnobUp(self, amount):
        return

    # @abc.abstractmethod
    def volumeKnobDown(self, amount):
        return

    def onConnect(self):
        self.speak("Online")

    def onDisconnect(self):
        self.speak("Offline")

    def speak(self, text):
        os.system('espeak -ven+f4 ' + re.escape(text) + ' &')
        # os.system('flite -voice slt -t "' + text + '"')

    def commandNotFound(self, command):
        ArmClient.commandNotFound(self, command)
        os.system("play -q -s -n synth tri %12 fade 0 1 1 &")

    def actionNotFound(self, action):
        ArmClient.actionNotFound(self, action)
        os.system("play -q -s -n synth tri %-36 fade 0 3 3 &")
