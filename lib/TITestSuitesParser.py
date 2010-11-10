#!/usr/bin/python

import os
import sys
import commands
import ConfigParser
import TIMessage

class TITestSuitesManager:

	class __impl:
		""" Implementation of the singleton interface """
		
		def spam(self):
			""" Test method, return singleton id """
			return id(self)

	__instance = None
	
	def __init__(self, settingsFile = None):
		
		if TITestSuitesManager.__instance is None:
			# Create and remember instance
			TITestSuitesManager.__instance = TITestSuitesManager.__impl()
			
			self.message = TIMessage.TIMessage(True)
			self.settingsFile = settingsFile
			self.configParser = None
			self.settings = {}
			self.readSettingsFile()
			self.parseSettings()

		self.__dict__['_TITestSuitesManager__instance'] = TITestSuitesManager.__instance
		
		return None

	def __getattr__(self, attr):
		""" Delegate access to implementation """
		return getattr(self.__instance, attr)

	def __setattr__(self, attr, value):
		""" Delegate access to implementation """
		return setattr(self.__instance, attr, value)
	
	def readSettingsFile(self):
		"""METHOD TITestSuitesManager.readSettingsFile
	Read settings file
	Input: None
	Output: None"""
		self.configParser = ConfigParser.ConfigParser()
		self.configParser.read(self.releaseFile)
		return None

	def getKeyValue(self, keyName):
		"""METHOD TITestSuitesManager.getKeyValue
	Get key value
	Input: keyName
	Output: keyValue"""
		return self.configParser.get(self.platformName, keyName)
