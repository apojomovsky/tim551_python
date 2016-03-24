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

class tim551():
    def __init__(self, ip, port, rangel = -45, rangeh = 225):
        self.host = ip
        self.port = port
        self.processed_data = []
        self.measures = []
        self.rangel = rangel
        self.rangeh = rangeh
        self._isReceiving = False

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
        if not self._isReceiving:
            self._isReceiving = True
            try:
                self.s.sendall("\x02sEN LMDscandata 1\x03\0")
            except socket.error:
                print 'Send failed'
                sys.exit()
            reply = self.s.recv(2048)
            #if "\x02sEA LMDscandata 1\x03" in reply:
            #    print "Started receiving data from sensor"
        else:
            print "Already receiving data from sensor"

    def stopReceivingData(self):
        if self._isReceiving:
            try:
                self.s.sendall("\x02sEN LMDscandata 0\x03\0")
            except socket.error:
                print 'Send failed'
                sys.exit()
            reply = self.s.recv(2048)
            #if "\x02sEA LMDscandata 0\x03" in reply:
            #    print "Stopped receiving data from sensor"
            self._isReceiving = False

    def singleDataRead(self):
        if not self._isReceiving:
            self._isReceiving = True
            try:
                self.s.sendall("\x02sRN LMDscandata\x03\0")
            except socket.error:
                print 'Send failed'
            self.readData()
            self._isReceiving = False
            return self.readDistances()

    def readData(self):
        self.data = self.s.recv(2048)

    def readDistances(self):
        try:
            self.processed_data = re.compile('\w+').findall(self.data)
            self.measures = [int(x, 16) for x in self.processed_data[26+45+self.rangel:297-225+self.rangeh]]
        except:
            pass
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
    parser.add_argument('-d', '--debug', action='store',
                        dest='debug', default=0,
                        help="Enables debug logs")
    parser.add_argument('-rl', '--range-low', action='store', type=int,
                        dest='rangel', default=-45,
                        help="Range Low")
    parser.add_argument('-rh', '--range-high', action='store', type=int,
                        dest='rangeh', default=225,
                        help="Range High")
    args = parser.parse_args()
    lidar = tim551(args.ip_address, args.port, args.rangel, args.rangeh)
    lidar.connect()
    #print lidar.singleDataRead()
    lidar.startReceivingData()
    for i in range(1):
        lidar.readData()
        print lidar.readDistances()
    #lidar.stopReceivingData()
