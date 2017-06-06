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
import sys
import platform
import ctypes
import glob
import threading
import numpy as np
import string

from random import shuffle
from array import *
from ctypes import *
from __builtin__ import exit

global condition1
global condition2
condition1 = False
condition2 = False


def setupData(): #Ask for the desired channels then asign them a thread task
				 #for each of them
		return 0

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
		return [imageNST, image]    #return a list of all the nonstimuli surface 
									 #all a list of all the surface
		
def sampling(actualchannellist):#Fonction ran by the data thread that put the
							        #acquired data in a global matrice for the
							        #selected channel
		
		IEE_EmoEngineEventCreate = libEDK.IEE_EmoEngineEventCreate
		IEE_EmoEngineEventCreate.restype = c_void_p
		eEvent = IEE_EmoEngineEventCreate()
	
		IEE_EmoEngineEventGetEmoState = libEDK.IEE_EmoEngineEventGetEmoState
		IEE_EmoEngineEventGetEmoState.argtypes = [c_void_p, c_void_p]
		IEE_EmoEngineEventGetEmoState.restype = c_int

		IEE_EmoStateCreate = libEDK.IEE_EmoStateCreate
		IEE_EmoStateCreate.restype = c_void_p
		eState = IEE_EmoStateCreate()
		
		userID = c_uint(0)
		user   = pointer(userID)
		ready  = 0
		state  = c_int(0)

		alphaValue     = c_double(0)
		low_betaValue  = c_double(0)
		high_betaValue = c_double(0)
		gammaValue     = c_double(0)
		thetaValue     = c_double(0)

		alpha     = pointer(alphaValue)
		low_beta  = pointer(low_betaValue)
		high_beta = pointer(high_betaValue)
		gamma     = pointer(gammaValue)
		theta     = pointer(thetaValue)

		
		if libEDK.IEE_EngineConnect("Emotiv Systems-5") != 0:
			print "Emotiv Engine start up failed."
			exit();

		print "Theta, Alpha, Low_beta, High_beta, Gamma \n"
		
		global condition1
		global condition2
		global matrice
		
		matrice = np.zeros((len(actualchannellist), 6, 1))
		matrice.astype(float)
		
		channeldic = {'AF3': 3, "F7": 4, 'F3': 5, 'FC5': 6, #dictionary containning
					'T7': 7, 'P7' : 8, 'PZ' : 9, 'O1' : 10, #the channels' 
					'O2': 11, 'P8': 12, 'T8': 13, 'FC6': 14,
					'F4': 15, 'F8': 16, 'AF4': 17}         	#respective list number
		channelnumberlist = []			
		
		for i in range(len(actualchannellist)): #make the list of the actual 
			channelnumberlist.append(channeldic[actualchannellist[i]]) #channels'
																	   #numbers 
		print channelnumberlist
		condition2 = True
		while condition1 == False:
			state = libEDK.IEE_EngineGetNextEvent(eEvent)
    
			if state == 0:
				eventType = libEDK.IEE_EmoEngineEventGetType(eEvent)
				libEDK.IEE_EmoEngineEventGetUserId(eEvent, user)
				#if eventType == 16:  # libEDK.IEE_Event_enum.IEE_UserAdded
				#	ready = 1
				#	libEDK.IEE_FFTSetWindowingType(userID, 1);  # 1: libEDK.IEE_WindowingTypes_enum.IEE_HAMMING
				#	print "User added"
                        
				if ready == 0:
					newdatamatrice = np.zeros((len(actualchannellist), 6, 1))
					newdatamatrice.astype(float)
					for i in range(len(actualchannellist)):
						result = c_int(0)
						print channeldic[actualchannellist[i]]
						result = libEDK.IEE_GetAverageBandPowers(userID, channelnumberlist[i], theta, alpha, low_beta, high_beta, gamma)
						actualtime = float(time.time())
						newdatamatrice[i,::,0] = (actualtime, thetaValue.value,
						alphaValue.value, low_betaValue.value, high_betaValue.value,
						gammaValue.value)
							
					matrice = np.concatenate((matrice, newdatamatrice),2)
							
			elif state != 0x0600:
				print "Internal error in Emotiv Engine ! "
			time.sleep(0.1)
		print "out"
	

			
class Picture(object):
	def __init__(self):
		self.__picture =setupimage()
		

	def afficher(self):
		pygame.init()	
		L = len(self.__picture[1])
		r = list(range(L))
		shuffle(r)
		while condition2 == False:
			time.sleep(0.1)
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
		global condition1
		condition1 = True

class Data(object):
	def __init__(self):
		self.__Data = []
		
	def main(self):
		actualchannellist = self.InitChans()
		print actualchannellist
		sampling(actualchannellist)
		return 
		
	def InitChans(self): #receive channels names from keyboard and identity them. 
						 #return the channels names in a list
		channellist = ('AF3', "F7", 'F3', 'FC5', 'T7', 'P7', 'PZ', 'O1',
						'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4')
		chosenchans = raw_input("Which channels you want to sample?(put a comma between each) \n")
		channelname = ""
		newchannellist = []
		for i in range(len(chosenchans)):
			newchar = chosenchans[i]
			newchar = string.capitalize(newchar)
			found = 0
			if newchar == " ":
				time.sleep(0)
				#this condition is used to ignore spaces
			elif newchar == ",":  #uses the ',' as a marker to know when the 
								   #channel's name's border
				for j in range(len(channellist)):
					if channelname == channellist[j]:
						newchannellist.append(channellist[j])
						channelname = ""
						found = 1
						break
					
				if found == 0:
					print channelname, "is not a channel and therefore, will be ignored!"
					channelname = ""
			elif i == len(chosenchans)-1 :
				channelname = channelname+newchar
				for j in range(len(channellist)):
					if channelname == channellist[j]:
						newchannellist.append(channelname)
						channelname = ""
						found = 1
				if found == 0:	
					print channelname, "is not a channel and therefore, will be ignored!"
					channelname = ""
			else:
				channelname = channelname + newchar
		condition2 = True
		return newchannellist
		
		
		
if __name__ == '__main__':
	if sys.platform.startswith('win32'):
	
		import msvcrt
	elif sys.platform.startswith('linux'):
		import atexit
		from select import select

	from ctypes import *

	try:
		if sys.platform.startswith('win32'):
			libEDK = cdll.LoadLibrary("/community-sdk/bin/win32/edk.dll")
		elif sys.platform.startswith('linux'):
		 	srcDir = os.getcwd()
		 	if platform.machine().startswith('arm'):
				libPath = srcDir + "/community-sdk/bin/armhf/libedk.so"
			else:
				libPath = srcDir + "/community-sdk/bin/linux64/libedk.so"
			libEDK = CDLL(libPath)
		else:
			raise Exception('System not supported.')
	except Exception as e:
		print 'Error: cannot load EDK lib:', e
		exit()
	
	np.set_printoptions(threshold=np.inf)
	
	global matrice	
	pic=Picture()
	data=Data()
	data1 = threading.Thread(target = data.main)
	pic1 = threading.Thread(target = pic.afficher)
	#data1.setDaemon(True)

	data1.start()
	pic1.start()
	pic1.join()
	

	print matrice
	
	

	
