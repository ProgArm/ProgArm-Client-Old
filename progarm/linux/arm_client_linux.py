from ..arm_client import ArmClient
from progarm import morse_codes
import os
import re
from os.path import dirname
# import abc

class ArmClientLinux(ArmClient):
    # __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(ArmClientLinux, self).__init__("/dev/rfcomm0")

        self.addAction(morse_codes.MORSE_M, "amixer set Master toggle")

        self.addAction(morse_codes.MORSE_N, dirname(__file__) + "/cmus_next &")
        self.addAction(morse_codes.MORSE_B, "cmus-remote --prev &")
        self.addAction(morse_codes.MORSE_C, dirname(__file__) + "/cmus_pause &")
        self.addAction(morse_codes.MORSE_A, self.cmusToggleAaa)

        self.addAction(morse_codes.MORSE_T, "amixer set Master playback 10%+ &")
        self.addAction(morse_codes.MORSE_E, "amixer set Master playback 10%- &")

        self.addAction(morse_codes.MORSE_W, dirname(__file__) + "/tell_time &")
        self.addAction(morse_codes.MORSE_D, dirname(__file__) + "/tell_date &")

    def processData(self, command):
        if command == "V":  # EXPERIMENTAL
            ticks = ord(self.serial.read())
            if ticks > 127:  # negative numbers # TODO 127 ?
                self.volumeKnobDown(255 - ticks)
            else:
                self.volumeKnobUp(ticks)
        else: # TODO remove else clause to allow further processing?
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
