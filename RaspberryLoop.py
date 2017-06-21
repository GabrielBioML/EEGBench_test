#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  RaspberryLoop.py
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
import RingBuffer
import sys
import platform
import ctypes
import glob
import threading
import multiprocessing
import numpy             as np
import string
import matplotlib.pyplot as plt

from Picture     import _Picture_
from RingBuffer  import RingBuffer
from random      import shuffle
from array       import *
from ctypes      import *
from __builtin__ import exit

class Data(object):
	def __init__(self):
		self.__Channels              = self.setupData()
		self.__DataStimulation   = _Picture_()
		self.__DataProcess       = self.DataProcess()
		self.__DataThreads       = self.DataThreads()
		self.__DataRingBuffer    = RingBuffer(2000,10,6)
		self.__DataQueue         = multiprocessing.Queue()
		self.__SampleRate        = 10 #Hertz
	def setupData(self): #Initialisation des canaux
		 #receive channels names from keyboard and idenfity them. 
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
		print type(newchannellist)
		return newchannellist
	
	def DataProcess(self):
		self.__process = multiprocessing.Process(target = self.DataSample, )
		
	def DataThreads(self):
		self.__DataRead   = threading.Thread(target = self.DataRead, )
		self.__DataWrite  = threading.Thread(target = self.DataWrite,)
		self.__DataImages = threading.Thread(target = self.__DataStimulation.afficher, )
	
	def DataRead(self):
		#Fonction qui envoiera les donnees a l'ordinateur
		while True:		
			data    = self.__DataRingBuffer.Reader()
			print data
			
	def DataWrite(self):
		while True:  #Mets les donnees du casque dans un buffer
			
			data    = self.__DataQueue.get()
			self.__DataRingBuffer.Writer(data)
			print "Wrote!"
		
	def DataSample(self): #channelList est la liste des noms des canaux choisis
		#quickly sample the headset (READ) signal
		
			IEE_EmoEngineEventCreate         = libEDK.IEE_EmoEngineEventCreate
			IEE_EmoEngineEventCreate.restype = c_void_p
			eEvent                           = IEE_EmoEngineEventCreate()
	
			IEE_EmoEngineEventGetEmoState          = libEDK.IEE_EmoEngineEventGetEmoState
			IEE_EmoEngineEventGetEmoState.argtypes = [c_void_p, c_void_p]
			IEE_EmoEngineEventGetEmoState.restype  = c_int

			IEE_EmoStateCreate         = libEDK.IEE_EmoStateCreate
			IEE_EmoStateCreate.restype = c_void_p
			eState                     = IEE_EmoStateCreate()
		
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
		
			i = 0
			L = len(self.__Channels)
			channel = {'AF3': 3, "F7" : 4, 'F3' : 5, 'FC5' : 6, 'T7' : 7, 'P7' : 8, 'PZ' : 9, 'O1' : 10,
						'O2' : 11, 'P8' : 12, 'T8' : 13, 'FC6' : 14, 'F4' : 15, 'F8' : 16, 'AF4' : 17}
		
			if libEDK.IEE_EngineConnect("Emotiv Systems-5") != 0:
				print "Emotiv Engine start up failed."
				exit();

			print "Theta, Alpha, Low_beta, High_beta, Gamma \n"		
			while True:
				
				state = libEDK.IEE_EngineGetNextEvent(eEvent)
				if state == 0:
					eventType = libEDK.IEE_EmoEngineEventGetType(eEvent)
					libEDK.IEE_EmoEngineEventGetUserId(eEvent, user)
		
					if ready == 0:
						Data = c_int(0)
						Data = libEDK.IEE_GetAverageBandPowers(userID, channel[self.__Channels[i]], theta, alpha, low_beta, high_beta, gamma)
						if Data == 0:
							self.__DataQueue.put(np.array([channel[self.__Channels[i]], thetaValue.value, alphaValue.value, low_betaValue.value, high_betaValue.value, gammaValue.value]))
							i = (i+1)%L
		
	def Main(self):

		
		self.__DataImages.start()
		self.__process.start()
		self.__DataRead.start()
		self.__DataWrite.start()
		
		self.__DataImages.join()
		self.__process.join()
		self.__DataRead.join()
		self.__DataWrite.join()
		
		
		return 0
		

def main():

	

	data = Data()
	data.Main()
	return 0

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
	main()

