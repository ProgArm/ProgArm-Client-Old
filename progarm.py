#!/usr/bin/env python
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

import optparse  # TODO derecated since Python 2.7, consider switching to argparse
import platform
import socket
#import os
from progarm.linux.maemo.arm_client_maemo import ArmClientMaemo
from progarm.linux.pc.arm_client_linux_pc import ArmClientLinuxPc


def main():
    parser = optparse.OptionParser()
    parser.add_option('-t', '--type', type='choice', choices=["gnu", "linux", "gnu/linux", "maemo", "n900"],
                      help='Specify client type.', dest='clientType', action='store')

    (opts, args) = parser.parse_args()

    clientClass = None
    if opts.clientType:  # type is specified manually
        if opts.clientType.lower() in ("gnu", "linux", "gnu/linux"):
            clientClass = ArmClientLinuxPc
        elif opts.clientType.lower() in ("maemo", "n900"):
            clientClass = ArmClientMaemo

    else:  # type not specified, trying to guess it
        if platform.system() == "Linux":
            if socket.gethostname() == "Nokia-N900":
            #if os.uname()[1] == "Nokia-N900":
                clientClass = ArmClientMaemo
            else:
                clientClass = ArmClientLinuxPc
        else:
            raise Exception("Cannot guess client type, try specifying it manually. See -h for more info.")

    clientClass().start()

if __name__ == "__main__":
    main()
