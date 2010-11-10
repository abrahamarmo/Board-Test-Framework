#!/usr/bin/python

import os
import TIMessage

class TIReport:

	class __impl:
		""" Implementation of the singleton interface """
		def spam(self):
			""" Test method, return singleton id """
			return id(self)

	__instance = None

	def __init__(self, path = None):
		if TIReport.__instance is None:
			# Create and remember instance
			TIReport.__instance = TIReport.__impl()
	
			self.message = TIMessage.TIMessage(True)
			self.path = path
			
			
			self.__dict__['_TIReport__instance'] = TIReport.__instance
		
		return None

	def __getattr__(self, attr):
		""" Delegate access to implementation """
		return getattr(self.__instance, attr)

	def __setattr__(self, attr, value):
		""" Delegate access to implementation """
		return setattr(self.__instance, attr, value)		
		
	def setDirectoryPath(self):
		"""METHOD TIReport.setDirectoryPath
	
	Input: directoryPath
	Output: None"""
		self.directoryPath = directoryPath	
		return None

	def getDirectoryPath(self):
		"""METHOD TIReport.getDirectoryPath
	
	Input: None
	Output: None"""
		return None
		
	def setDirectoryName(self):
		"""METHOD TIReport.setDirectoryName(
	
	Input: directoryName
	Output: None"""
		self.directoryName = directoryName 
		return None

	def getDirectoryName(self):
		"""METHOD TIReport.getDirectoryName
	
	Input: None
	Output: None"""
		return None		

	def createDirectory(self):
		"""METHOD TIReport.getDirectoryPath
	
	Input: None
	Output: None"""
		try:
			os.mkdir(os.join(self.directoryPath, self.directoryName))
		except Exception,error:
			self.message.ERROR('Directory exists!')
		return None
