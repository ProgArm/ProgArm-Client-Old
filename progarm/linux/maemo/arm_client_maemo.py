from ..arm_client_linux import ArmClientLinux
from progarm import morse_codes
import os
from os.path import dirname

class ArmClientMaemo(ArmClientLinux):
    def __init__(self):
        super(ArmClientMaemo, self).__init__()
        self.addAction(morse_codes.MORSE_P, dirname(__file__) + "/call_answer &")
        self.addAction(morse_codes.MORSE_R, dirname(__file__) + "/call_release &")
        self.addAction(morse_codes.MORSE_M, dirname(__file__) + "/mute &")
        self.addAction(morse_codes.MORSE_S, dirname(__file__) + "/beep &")

    def volumeKnobUp(self, amount):
        os.system("./volumeKnob +" + str(amount))

    def volumeKnobDown(self, amount):
        os.system("./volumeKnob -" + str(amount))
