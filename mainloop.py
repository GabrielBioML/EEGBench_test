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
import threading

def setupimage(): #load the picture that will be used
		
		liste = glob.glob('/home/pi/Documents/EEGBench_test/Images/stimuli*') #find all the pictures that represent a stimuli
		n = len(liste)
		image=[None] * n
		for i in range (0,n):
			image[i]= pygame.image.load(os.path.join(liste[i]))
		liste = glob.glob('/home/pi/Documents/EEGBench_test/Images/nonstimuli*') #find all the pictures that represent a non-stimuli
		l = len(liste)
		imageNST=[None] * l
		for i in range (0,l):
			imageNST[i]= pygame.image.load(os.path.join(liste[i]))
		image.extend(imageNST)
		return [imageNST, image]    #return a list of all the nonstimuli surface all a list of all the surface
		
def wait(temps):
	a = time.clock() + temps
	b = 0
	while b < a:
			b = time.clock()			
			
class Picture(object):
	def __init__(self):
		self.__picture =setupimage()
		

	def afficher(self):
		pygame.init()
		a = time.time()	
		L = len(self.__picture[1])
		r = list(range(L))
		shuffle(r)
		for i in r:
			screen = pygame.display.set_mode((1824, 984))
			screen.blit(self.__picture[1][i], (0,0))
			pygame.display.flip()
			NST = len(self.__picture[1])-len(self.__picture[0])
			if i < NST:
				print "stimuli!!!"
			else:
				print "non stimuli"
			self.__picture[1][i].unlock()
			time.sleep(1)
		print a

class Data(object):
	def __init__(self):
		self.__Data = setupData()
		
	def main(self):
            while True:
		b = time.time()
		print "success!", b
		time.sleep(2)

def setupData():
	return 0
		
		
		
		
if __name__ == '__main__':
	pic=Picture()
	data=Data()
	data1 = threading.Thread(target = data.main)
        pic1 = threading.Thread(target = pic.afficher)
        data1.setDaemon(True)

	data1.start()
	pic1.start()

	pic1.join()
	

	
