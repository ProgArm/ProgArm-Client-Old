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
from progarm import input_codes
import os
from os.path import dirname


class ArmClientMaemo(ArmClientLinux):
    def __init__(self):
        super(ArmClientMaemo, self).__init__()
        self.addAction(input_codes.INPUT_P, dirname(__file__) + "/call_answer &")
        self.addAction(input_codes.INPUT_R, dirname(__file__) + "/call_release &")
        self.addAction(input_codes.INPUT_M, dirname(__file__) + "/mute &")
        self.addAction(input_codes.INPUT_S, dirname(__file__) + "/beep &")

    def volumeKnobUp(self, amount):
        os.system("./volumeKnob +" + str(amount))

    def volumeKnobDown(self, amount):
        os.system("./volumeKnob -" + str(amount))
