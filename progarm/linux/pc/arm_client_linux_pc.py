# Copyright (C) 2014  Alex-Daniel Jakimenko <alex.jakimenko@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# THIS program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from ..arm_client_linux import ArmClientLinux
from progarm import input_codes
import os
import pipes


class ArmClientLinuxPc(ArmClientLinux):
    def __init__(self):
        super(ArmClientLinuxPc, self).__init__()
        self.addAction(input_codes.INPUT_F, "xte 'keydown Alt_L' 'key F4' 'keyup Alt_L' &")
        self.addAction(input_codes.INPUT_M, "amixer set Master toggle &")
        #self.addAction(input_codes.INPUT_B, "beep &")
        self.addAction(input_codes.INPUT_R, "xdotool key Right &")
        self.addAction(input_codes.INPUT_Z, "xdotool key Left &")

    def volumeKnobUp(self, amount):
        os.system("amixer set Master playback " + str(amount) + "%+ > /dev/null")

    def volumeKnobDown(self, amount):
        os.system("amixer set Master playback " + str(amount) + "%- > /dev/null")

    def plainTextReceived(self, str):
        os.system("notify-send " + pipes.quote(str))
