#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  mainloop.py
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
import glob
from random import shuffle

def setupimage(): #load the picture that will be used
		
		liste = glob.glob('/home/pi/Documents/EEGBench_test/Images/picture*')
		n = len(liste)
		image=[None] * n
		shuffle(liste)
		#namespace = globals()
		for i in range (0,n-1):
			#namespace['image_%d' % i] 
			image[i]= pygame.image.load(os.path.join(liste[i+1]))
		return image
			
			
class Picture(object):
	def __init__(self):
		self.__picture=setupimage()
		
	def wait(self,temps):
		a = time.clock() + temps
		b = 0
		while b < a:
				b = time.clock()


	def main(self):
		#self.setupimage()
		pygame.init()
		a = time.time()	
		#image = pygame.image.load(os.path.join('/home/pi/Documents/EEGBench_test/Images/picture_1.jpg'))
		screen = pygame.display.set_mode((1824, 984))
		screen.blit(self.__picture[2], (0,0))
		pygame.display.flip()
		self.wait(3)
		
if __name__ == '__main__':
	pic=Picture()
	pic.main()

