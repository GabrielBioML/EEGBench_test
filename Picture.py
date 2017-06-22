#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Picture.py
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

import pygame
import os
import time
import sys
import platform
import ctypes
import glob

from random import shuffle

def setupimage(): #load the picture that will be used
		n = 5 #nombre de stimuli
		stimuli = glob.glob('/home/pi/Documents/EEGBench_test/Images/stimuli*') #find all the pictures that represent a stimuli
		image = [pygame.image.load(os.path.join(stimuli[0]))] * n
		liste = glob.glob('/home/pi/Documents/EEGBench_test/Images/nonstimuli*') #find all the pictures that represent a non-stimuli
		l = len(liste)
		imageNST=[None] * l * n
		for i in range (0,l):
			for j in range(n):
				imageNST[i + (j*l)]= pygame.image.load(os.path.join(liste[i]))
		image.extend(imageNST)
		info = [pygame.image.load(os.path.join('/home/pi/Documents/EEGBench_test/Images/StarttestA.png')), pygame.image.load(os.path.join('/home/pi/Documents/EEGBench_test/Images/Interlude.png'))]
		return [imageNST, image, info]    #return a list of all the nonstimuli surface 
									 #all a list of all the surface

class _Picture_(object):
	def __init__(self):
		self.__picture =setupimage()
		

	def afficher(self): #, start, stop, flagstimuli, flagnonstimuli, ):
		#stop.clear()
		#flagstimuli.clear()
		#flagnonstimuli.clear()
		pygame.init()	
		L = len(self.__picture[1])
		r = list(range(L))
		shuffle(r)
		#start.wait()
		screen = pygame.display.set_mode((1824, 984))
		screen.blit(self.__picture[2][0], (0,0))
		pygame.display.flip()
		time.sleep(15)
		for i in r:
			screen = pygame.display.set_mode((1824, 984))
			screen.blit(self.__picture[1][i], (0,0))
			pygame.display.flip()
			NST = len(self.__picture[1])-len(self.__picture[0])
			"""
			if i < NST:
				flagstimuli.set()
			else:
				flagnonstimuli.set()
			"""
			self.__picture[1][i].unlock()
			time.sleep(1)
			screen.blit(self.__picture[2][1], (0,0))
			pygame.display.flip()
			time.sleep(1)
		#stop.set()
