#!/usr/bin/python

import os
import sys
import commands
import ConfigParser
import TIMessage

class TISettingsManager:

	class __impl:
		""" Implementation of the singleton interface """
		
		def spam(self):
			""" Test method, return singleton id """
			return id(self)

	__instance = None
	
	def __init__(self, settingsFile = None):
		
		if TISettingsManager.__instance is None:
			# Create and remember instance
			TISettingsManager.__instance = TISettingsManager.__impl()
			
			self.message = TIMessage.TIMessage(True)
			self.settingsFile = settingsFile
			self.configParser = None
			self.settings = {}
			self.readSettingsFile()
			self.parseSettings()

		self.__dict__['_TISettingsManager__instance'] = TISettingsManager.__instance
		
		return None
		
	def __getattr__(self, attr):
		""" Delegate access to implementation """
		return getattr(self.__instance, attr)

	def __setattr__(self, attr, value):
		""" Delegate access to implementation """
		return setattr(self.__instance, attr, value)

	def readSettingsFile(self):
		"""METHOD TISettingsManager.readSettingsFile
	Read settings file
	Input: None
	Output: None"""
		self.configParser = ConfigParser.ConfigParser()
		self.configParser.read(self.settingsFile)
		return None
	
	def parseSettings(self):
		"""METHOD TISettingsManager.parseSettings
	Parse settings
	Input: None
	Output: None"""
		self.configParser.sections()
		for onesection in self.configParser.sections():
			for oneoption in self.configParser.options(onesection):
				self.settings[oneoption] = self.configParser.get(onesection, oneoption)			
		return None

	def setKeyValue(self, keyName, keyValue):
		"""METHOD TISettingsManager.setKey
	Set key value
	Input: keyName keyValue
	Output: None"""
		self.settings[keyName] = keyValue
		return None
		
	def getKeyValue(self, keyName):
		"""METHOD TISettingsManager.getKey
	Get key value
	Input: keyName
	Output: keyValue"""
		return self.settings[keyName]

	def getAllOptions(self, sectionName):
		"""METHOD TISettingsManager.getAllOptions
	Get all options
	Input: sectionName
	Output: None"""
		return self.configParser.options(sectionName)
	
