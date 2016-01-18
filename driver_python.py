#!/usr/bin/env python
#
#  Copyright 2016 Alexis Pojomovsky <apojomovsky@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import socket
import sys
ADDR = '169.254.73.213'
PORT = 2112


class tim551:
    def __init__(self, ip, port):
        self.host = ip
        self.port = port

    def connect(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print 'Failed to create socket'
            sys.exit()
        print 'Socket Created'
        try:
            remote_ip = socket.gethostbyname(self.host)
        except socket.gaierror:
            print 'Hostname could not be resolved. Exiting'
            sys.exit()
        # Connect to remote server
        self.s.connect((remote_ip, self.port))
        print 'Socket Connected to ' + self.host + ' on ip ' + remote_ip

    def startReceivingData(self):
        message = "\x02sEN LMDscandata 1\x03\0"
        try:
            self.s.sendall(message)
        except socket.error:
            print 'Send failed'
            sys.exit()
        reply = self.s.recv(4096)
        print reply
        if reply is "sEA LMDscandata 1":
            print "EL RIO DE LA CACAAAAA"
        data = self.s.recv(2048)
        print data

    def stopReceivingData(self):
        message = "\x02sEN LMDscandata 0\x03\0"
        try:
            self.s.sendall(message)
        except socket.error:
            print 'Send failed'
            sys.exit()
        print 'Stopped receiving data from sensor'
        reply = self.s.recv(4096)
        print reply

    def close(self):
        self.s.close()


if __name__ == '__main__':
    lidar = tim551(ADDR, PORT)
    lidar.connect()
    lidar.startReceivingData()
    lidar.stopReceivingData()
    lidar.close()
