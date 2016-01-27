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

from sick_lidar import tim551
import matplotlib.pyplot as plt
import numpy as np

ADDR = '169.254.73.213'
PORT = 2112


if __name__ == '__main__':
    lidar = tim551(ADDR, PORT)
    lidar.connect()
    lidar.startReceivingData()
    lidar.readData()
    lidar.readDistances()
    ax = plt.subplot(111, projection='polar')
    ax.plot(np.arange(271)*2*np.pi/360, np.asarray(lidar.readDistances()), color='r', linewidth=1)
    ax.grid(True)
    plt.show()