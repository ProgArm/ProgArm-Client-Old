from arm_client_linux_pc import ArmClientLinuxPc
from progarm import morse_codes

class ArmClientLinuxPresentation(ArmClientLinuxPc):
    def __init__(self):
        super(ArmClientLinuxPresentation, self).__init__()
        self.addAction(morse_codes.MORSE_T, "xdotool key Left &")
        self.addAction(morse_codes.MORSE_E, "xdotool key Right &")