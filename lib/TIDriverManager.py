#!/usr/bin/python

import os
import sys
import commands
import ConfigParser
import TIMessage

class TIDriverManager:

	class __impl:
		""" Implementation of the singleton interface """
		def spam(self):
			""" Test method, return singleton id """
			return id(self)

	__instance = None

	def __init__(self):
		if TIDriverManager.__instance is None:
			# Create and remember instance
			TIDriverManager.__instance = TIDriverManager.__impl()
	
			self.message = TIMessage.TIMessage(True)
			self.driversFile = '../conf/driver.cfg'
			self.configParser = None
			self.readDriversFile()
		
		self.__dict__['_TIDriversManager__instance'] = TIDriverManager.__instance
		
		return None
		
	def __getattr__(self, attr):
		""" Delegate access to implementation """
		return getattr(self.__instance, attr)

	def __setattr__(self, attr, value):
		""" Delegate access to implementation """
		return setattr(self.__instance, attr, value)		
	
	def readDriversFile(self):
		"""METHOD TIDriverManager.readDriversFile
	Read settings file
	Input: None
	Output: None"""
		self.configParser = ConfigParser.ConfigParser()
		self.configParser.read(self.driversFile)
		return None

	def getKeyValue(self, driver, keyName):
		"""METHOD TIDriverManager.getKey
	Get key value
	Input: keyName
	Output: keyValue"""
		return self.configParser.get(driver, keyName)
		
	def getKeyValueOffset(self, driver, keyName, offset):
		"""METHOD TIDriverManager.getKeyValueOffset
	Get key value
	Input: keyName
	Output: keyValue"""	
		tempList = self.configParser.get(driver, keyName).split(';')
		return tempList[offset]
		
	
		
