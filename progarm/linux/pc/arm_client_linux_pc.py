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
