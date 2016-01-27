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
import argparse
import sys
import re

ADDR = '169.254.73.213'
PORT = 2112


class tim551:
    def __init__(self, ip, port, output):
        self.host = ip
        self.port = port
        self.output = output
        self.processed_data = []
        self.measures = []

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
        try:
            self.s.sendall("\x02sEN LMDscandata 1\x03\0")
        except socket.error:
            print 'Send failed'
            sys.exit()
        reply = self.s.recv(2048)
        if "\x02sEA LMDscandata 1\x03" in reply:
            print "Started receiving data from sensor"

    def stopReceivingData(self):
        try:
            self.s.sendall("\x02sEN LMDscandata 0\x03\0")
        except socket.error:
            print 'Send failed'
            sys.exit()
        reply = self.s.recv(2048)
        if "\x02sEA LMDscandata 0\x03" in reply:
            print "Stopped receiving data from sensor"

    def readData(self):
        self.data = self.s.recv(2048)

    def readDistances(self):
        self.processed_data = re.compile('\w+').findall(self.data)
        self.measures = [int(x, 16) for x in self.processed_data[26:297]]
        return self.measures

    def __del__(self):
        self.s.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Friendly driver for SICK TiM551 sensor')
    parser.add_argument('-i', '--ip-addr', action='store',
                        dest='ip_address', default=ADDR,
                        help="IP address of the sensor")
    parser.add_argument('-p', '--port', action='store', type=int,
                        dest='port', default=PORT,
                        help="Port number of the sensor")
    parser.add_argument('-o', '--output', action='store',
                        dest='output', default='console',
                        help="Outputs to console or a file")
    parser.add_argument('-d', '--debug', action='store',
                        dest='debug', default=0,
                        help="Enables debug logs")
    args = parser.parse_args()
    lidar = tim551(args.ip_address, args.port, args.output)
    lidar.connect()
    lidar.startReceivingData()
    for i in range(1):
        lidar.readData()
        lidar.readDistances()
    lidar.stopReceivingData()
