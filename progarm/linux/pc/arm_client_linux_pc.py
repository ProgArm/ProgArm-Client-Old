from ..arm_client_linux import ArmClientLinux
from progarm import morse_codes
import os

class ArmClientLinuxPc(ArmClientLinux):
    def __init__(self):
        super(ArmClientLinuxPc, self).__init__()
        self.addAction(morse_codes.MORSE_Q, "xte 'keydown Alt_L' 'key F4' 'keyup Alt_L' &")
        self.addAction(morse_codes.MORSE_M, "amixer set Master toggle &")
        self.addAction(morse_codes.MORSE_S, "beep &")

    def volumeKnobUp(self, amount):
        os.system("amixer set Master playback " + str(amount) + "%+ > /dev/null")

    def volumeKnobDown(self, amount):
        os.system("amixer set Master playback " + str(amount) + "%- > /dev/null")