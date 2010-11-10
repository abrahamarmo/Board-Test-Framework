#!/usr/bin/python

import os
import sys
import commands
import ConfigParser
import TIMessage


class Error(Exception):
    """Base class for ConfigParser exceptions."""

    def __init__(self, msg=''):
        self.message = msg
        Exception.__init__(self, msg)

    def __repr__(self):
        return self.message

    __str__ = __repr__
    
class NoPlatformNameError(Error):
    """Raised when no platform name matches a requested option."""

    def __init__(self, platformName):
        Error.__init__(self, 'No platform name: %r' % (platformName,))
        self.platformName = platformName
        
class NoModuleNameError(Error):
    """Raised when no module name matches"""
    def __init__(self, moduleName):
        Error.__init__(self, 'No module name: %r' % (moduleName,))
        self.moduleName = moduleName
        
class TIReleaseManager:

	class __impl:
		""" Implementation of the singleton interface """
		
		def spam(self):
			""" Test method, return singleton id """
			return id(self)

	__instance = None

	def __init__(self, platformName = None):

		if TIReleaseManager.__instance is None:
			# Create and remember instance
			TIReleaseManager.__instance = TIReleaseManager.__impl()

			self.message = TIMessage.TIMessage(True)
			
			self.releaseFile = '../conf/release.cfg'
			self.platformName = platformName
			self.moduleName = None
			self.configParser = None
			self.crossCompilerPrefix = None
			self.compilationSteps = None
			self.modulePath = None
			self.defconfigName = None
			
			self.readFile()
			self.setPlatformName()
			self.setCrossCompilerPrefix()
			self.setHostPrefix()
					
		self.__dict__['_TIReleaseManager__instance'] = TIReleaseManager.__instance
		
		return None
	
	def __getattr__(self, attr):
		""" Delegate access to implementation """
		return getattr(self.__instance, attr)

	def __setattr__(self, attr, value):
		""" Delegate access to implementation """
		return setattr(self.__instance, attr, value)

	def setPlatformName(self):
		"""METHOD TIReleaseManager.setPlatformName
	Set the name of the platform
	Input: None
	Output: None"""
		try:
			self.configParser.has_section(self.platformName)
		except ConfigParser.NoSectionError:
			self.message.FATAL('No section: %s' % self.platformName)
			raise NoPlatformNameError(self.platformName)
		return None
		
	def getPlatformName(self):
		"""METHOD TIReleaseManager.getPlatformName
	Get the name of the platform
	Input: None
	Output: None"""
		return self.platformName

	def setCrossCompilerPrefix(self):
		"""METHOD TIReleaseManager.setCrossCompilerPrefix
	Set the prefix of the cross compiler
	Input: None
	Output: None"""
		self.crossCompilerPrefix = self.getKeyValue('crossCompiler')
		return None

	def getCrossCompilerPrefix(self):
		"""METHOD TIReleaseManager.getCrossCompilerPrefix
	Get the prefix of the cross compiler
	Input: None
	Output: None"""
		return self.crossCompilerPrefix		

	def setHostPrefix(self):
		"""METHOD TIReleaseManager.setHostPrefix
	Set the prefix of the host
	Input: None
	Output: None"""
		self.hostPrefix = self.getKeyValue('host')
		return None

	def getHostPrefix(self):
		"""METHOD TIReleaseManager.getHostPrefix
	Get the prefix of the host
	Input: None
	Output: None"""
		return self.hostPrefix		
		
	def setModuleName(self, moduleName):
		"""METHOD TIReleaseManager.setModuleName
	Set the prefix of the cross compiler
	Input: None
	Output: None"""
		self.moduleName = moduleName
		self.setModulePath()
		self.setDefconfigName()
		self.setCompilationSteps()
		return None

	def getModuleName(self):
		"""METHOD TIReleaseManager.getModuleName
	Get the name of the module
	Input: None
	Output: None"""
		return self.moduleName

	def setModulePath(self):
		"""METHOD TIReleaseManager.setModulePath
	Set the module path
	Input: None
	Output: None"""
		self.modulePath = self.getKeyValue(self.moduleName+'Path')
		return None		

	def getModulePath(self):
		"""METHOD TIReleaseManager.getModulePath
	Get the module path
	Input: None
	Output: None"""
		return self.modulePath
		
	def setCompilationSteps(self):
		"""METHOD TIReleaseManager.setCompilationSteps
	Set Compilation Steps
	Input: None
	Output: None"""		
		compilationSteps = self.getKeyValue(self.moduleName+'steps')
		self.compilationSteps = compilationSteps.split(';')
		return None

	def getCompilationSteps(self):
		"""METHOD TIReleaseManager.getCompilationSteps
	Get Compilation Steps
	Input: None
	Output: compilationSteps"""
		return self.compilationSteps
		
	def setDefconfigName(self):
		"""METHOD TIReleaseManager.setDefconfigName
	Set the defconfig to use
	Input: None
	Output: None"""
		self.defconfigName = self.getKeyValue(self.moduleName+'DefConfig')
		return None

	def getDefconfigName(self):
		"""METHOD TIReleaseManager.getDefconfigName
	Get the defconfig to use
	Input: None
	Output: None"""
		return self.defconfigName
		
	def readFile(self):
		"""METHOD TIReleaseManager.readFile
	Read configuration file
	Input: None
	Output: None"""
		self.configParser = ConfigParser.ConfigParser()
		self.configParser.read(self.releaseFile)
		return None
		
	def getKeyValue(self, keyName):
		"""METHOD TIReleaseManager.getKeyValue
	Get key value
	Input: keyName
	Output: keyValue"""
		return self.configParser.get(self.platformName, keyName)
		
