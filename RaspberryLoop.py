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
import multiproccessing
import numpy             as np
import string
import matplotlib.pyplot as plt

from random      import shuffle
from array       import *
from ctypes      import *
from __builtin__ import exit

def setupimage(): #load the picture that will be used
		n       = 5 #nombre de stimuli
		stimuli = glob.glob('/home/pi/Documents/EEGBench_test/Images/stimuli*') #find all the pictures that represent a stimuli
		image   = [pygame.image.load(os.path.join(stimuli[0]))] * n
		liste   = glob.glob('/home/pi/Documents/EEGBench_test/Images/nonstimuli*') #find all the pictures that represent a non-stimuli
		l       = len(liste)
		imageNST=[None] * l * n
		for i in range (0,l):
			for j in range(n):
				imageNST[i + (j*l)]= pygame.image.load(os.path.join(liste[i]))
		image.extend(imageNST)
		info = [pygame.image.load(os.path.join('/home/pi/Documents/EEGBench_test/Images/StarttestA.png')), pygame.image.load(os.path.join('/home/pi/Documents/EEGBench_test/Images/Interlude.png'))]
		return [imageNST, image, info]    #return a list of all the nonstimuli surface 
									 #all a list of all the surface

class Data(object):
	def __init__(self):
		self.__Data            = self.setupData()
		self.__DataProcess     = self.DataProcess()
		self.__DataThreads     = self.DataThreads()
		self.__RingBuffer      = RingBuffer(2000,10,6)
		self.__DataStimulation = Picture()
		self.__DataQueue       = multiprocessing.queue()
		self.__ChannelQueue    = multiproccessing.queue()
		
	def setupData(self): #Initialisation des canaux
		 #receive channels names from keyboard and identity them. 
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
		return newchannellist
	
	def DataProcess(self):
		self.__process = multiproccessing.Process(DataRead, )
		self.__process.start
		
	def DataThreads(self):
		return 0
	
	def SendAnalysedData(self):
		#Fonction qui envoiera les donnees a l'ordinateur
		
		return 0
	
	def DataWrite(self, channelList):
		channel = self.__ChannelQueue.get()
		data    = self.__DataQueue.get()
		
		data.append(channel)
		
		RingBuffer.Writer(data)
		
	def DataRead(self, newchannellist): #channelList est la liste des numeros des canaux choisis
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
		
		
		while True:
			i    = (i+1)%L
			Data = libEDK.IEE_GetAverageBandPowers(userID, channelList[i], theta, alpha, low_beta, high_beta, gamma)
			self.__DataQueue.put(Data)
			self.__ChannelQueue.put(channel[i])
		
	def Main(self):
		
		return 0
		

def main():
	
	return 0

if __name__ == '__main__':
	main()

