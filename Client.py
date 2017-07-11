#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Client.py
#  
#  Copyright 2017  <pi@raspberrypi>
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

import sys
import socket

SERVER_IP = '192.168.1.108'
PORT_NUMBER = 5002
SIZE = 1024
print ("Test client sending packages to IP {0}, via port {1}\n".format(SERVER_IP, PORT_NUMBER))

mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
myMessage = "Hello"
myMessage1 = ""
i = 0

while i < 10:
	mySocket.sendto(myMessage.encode('utf-8'), (SERVER_IP,PORT_NUMBER))
	i += 1

mySocket.sendto(myMessage1.encode('utf-8'), (SERVER_IP,PORT_NUMBER))

sys.exit()
