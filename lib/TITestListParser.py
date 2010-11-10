#!/usr/bin/python

import os
import sys
import time
import tempfile
import TIMessage
import TIDriverManager
import TISettingsManager

class TITestListParser:

	class __impl:
		""" Implementation of the singleton interface """
		
		def spam(self):
			""" Test method, return singleton id """
			return id(self)

	__instance = None
	
	def __init__(self, testTypeRequest = None):
		
		if TITestListParser.__instance is None:
			# Create and remember instance
			TITestListParser.__instance = TITestListParser.__impl()
			
			self.message = TIMessage.TIMessage(True)
			self.drivers 	= TIDriverManager.TIDriverManager()			
			self.settings = TISettingsManager.TISettingsManager()
			self.testType = testTypeRequest
			
			self.testRunnerSintaxis = None
			self.logFileSintaxis = None
			self.stdOutFleSintaxis = None
			self.enabledDriver = []
			self.driver = None
			self.scenarioId = None
			self.testRunnerArguments = None
			self.uImageType = None
			self.scenariosList = []
			self.scenariosListAuto = []
			self.scenariosListManual = []
			self.builtScenariosList = []
			self.prefix = None
			self.tempFile = None
			self.logFile = None
		
			self.setEnabledDriverList()
			#self.setTestType()
			self.mainParser()
		
		self.__dict__['_TITestListParser__instance'] = TITestListParser.__instance
		
		return None
		
	def __getattr__(self, attr):
		""" Delegate access to implementation """
		return getattr(self.__instance, attr)

	def __setattr__(self, attr, value):
		""" Delegate access to implementation """
		return setattr(self.__instance, attr, value)

	def createTemporalFile(self):
		"""METHOD TITestListParser.createTemporalFile
	Create a temporal file
	Input: None
	Output: None"""
		self.tempFile = tempfile.mktemp()
		self.logFile = open(self.tempFile, "w+b")
		os.chmod(self.tempFile , 0777)
		return None
		
	def getTemporalFile(self):
		"""METHOD TITestListParser.getTemporalFile
	Create a temporal file
	Input: None
	Output: None"""
		return self.tempFile


	def writeScenariosToFile(self, LOG=None):
		"""METHOD TITestListParser.writeScenariosToFile
	Write Scenarios To File
	Input: None
	Output: None"""
		if self.getScenariosList():
			self.setBuiltScenariosList()
			for eachscenario in self.builtScenariosList:
				self.scenarioId = eachscenario
				self.setLogFileSintaxis()
				self.setStdOutFileSintaxis()
				tmpCmd = '%s %s %s %s %s' % (self.getTestRunnerSintaxis(), \
																		self.getLogFileSintaxis(), \
																		self.getStdOutFileSintaxis(), \
																		self.getTestRunnerArguments(), \
																		eachscenario)
				if not LOG:
					self.logFile.write('\n'+tmpCmd)
				else:
					self.logFile.write('\n'+'# manual > '+tmpCmd)
					
	def mainParser(self):
		"""METHOD TITestListParser.mainParser
	
	Input: None
	Output: None"""				
		
		self.createTemporalFile()
		self.logFile.write('#!/bin/sh')
		self.logFile.write('\n\n# Copy dmesg to test results directory')
		self.logFile.write('\ncp /var/log/dmesg /automation/testresults')
		self.logFile.write('\n\n# Sleep for 5 seconds')
		self.logFile.write('\nsleep 5')
		
		if self.testType != 'auto' and self.testType != 'manual':
			self.logFile.write('\n\n# Bring eth0 interface down')
			self.logFile.write('\n\nifconfig eth0 down')
			self.logFile.write('\n\n/%s.sh' % self.testType)

		else:

			for eachdriver in self.enabledDriver:
				
				self.logFile.write('\n\n# [%s]' % eachdriver)
				
				self.driver = eachdriver
				self.setTestRunnerSintaxis()
				self.setTestRunnerArguments()
				self.setPrefix()
				self.setScenariosList()
					
				autoList, manualList = self.getScenariosList()
			
				if self.testType == 'manual':
					self.scenariosList = 	manualList
					self.setBuiltScenariosList()
					self.writeScenariosToFile(LOG='Y')
					self.scenariosList = 	autoList
					self.setBuiltScenariosList()
					self.writeScenariosToFile()
					
					
				elif self.testType == 'auto':
				
					self.scenariosList = 	autoList
					self.setBuiltScenariosList()
					self.writeScenariosToFile()


		self.logFile.write('\n\nchmod -R 777 /automation/testresults')
		
		if self.testType != 'manual':
			self.logFile.write('\n\nreboot')
		self.logFile.close()
		return None
		
	def setTestType(self):
		"""METHOD TITestListParser.setTestType
	
	Input: None
	Output: None"""
		if self.testType == 'auto' or self.testType == 'manual':
			self.testType = self.testType
		else:
			self.testType = 'auto'
		return None 
		
	def setEnabledDriverList(self):
		"""METHOD TITestListParser.setEnabledDriverList
	
	Input: None
	Output: None"""
		drivers = self.settings.getAllOptions('drivers')
		if self.testType == 'auto' or self.testType == 'manual':
			for eachdriver in drivers:
				if self.settings.getKeyValue(eachdriver) == 'y' and \
						eachdriver != 'utils' and eachdriver != 'lmbench':
					self.enabledDriver.append(eachdriver)
		else:
			self.enabledDriver.append('lmbench')
		return None

	def getEnabledDriverList(self):
		"""METHOD TITestListParser.getEnabledDriverList
	
	Input: None
	Output: None"""
		return self.enabledDriver
		
	def setTestRunnerSintaxis(self):
		"""METHOD TITestListParser.setTestRunnerSintaxis
	
	Input: None
	Output: None"""
		self.testRunnerSintaxis = '/automation/testsuites/%s/scripts/test_runner.sh'\
															 % self.driver
		return None
	
	def getTestRunnerSintaxis(self):
		"""METHOD TITestListParser.getTestRunnerSintaxis
	
	Input: None
	Output: None"""
		return self.testRunnerSintaxis
	
	def setLogFileSintaxis(self):
		"""METHOD TITestListParser.setLogFileSintaxis
	
	Input: None
	Output: None"""
		self.logFileSintaxis = '-l /automation/testresults/%s.log'\
														% self.scenarioId
		return None
		
	def getLogFileSintaxis(self):
		"""METHOD TITestListParser.getLogFileSintaxis
	
	Input: None
	Output: None"""
		return self.logFileSintaxis
		
	def setStdOutFileSintaxis(self):
		"""METHOD TITestListParser.setStdOutFileSintaxis
	
	Input: None
	Output: None"""
		self.stdOutFileSintaxis = '-o /automation/testresults/%s.stdout'\
														% self.scenarioId
		return None
		
	def getStdOutFileSintaxis(self):
		"""METHOD TITestListParser.getStdOutFileSintaxis
	
	Input: None
	Output: None"""
		return self.stdOutFileSintaxis

	def setuImageType(self):
		"""METHOD TITestListParser.setuImageType
	
	Input: None
	Output: None"""
		self.uimageType = self.drivers.getKeyValueOffset(self.driver, self.testType, 0) 
		return None

	def getuImageType(self):
		"""METHOD TITestListParser.getuImageType
	
	Input: None
	Output: None"""
		return self.uimageType 
		
	def setTestRunnerArguments(self):
		"""METHOD TITestListParser.setTestRunnerArguments
	
	Input: None
	Output: None"""
		self.testRunnerArguments = self.drivers.getKeyValueOffset(self.driver, self.testType, 1)
		return None
		
	def getTestRunnerArguments(self):
		"""METHOD TITestListParser.getTestRunnerArguments
	
	Input: None
	Output: None"""
		return self.testRunnerArguments

	def setScenariosList(self):
		"""METHOD TITestListParser.setScenariosList
	
	Input: None
	Output: None"""
		
		self.scenariosListAuto = []
		self.scenariosListManual = []
		
		self.scenariosListAuto = self.drivers.getKeyValueOffset(self.driver, 'auto', 2)
		if self.scenariosListAuto:
			self.scenariosListAuto = self.scenariosListAuto.split(',')
		
		self.scenariosListManual = self.drivers.getKeyValueOffset(self.driver, 'manual', 2)
		if self.scenariosListManual:
			self.scenariosListManual = self.scenariosListManual.split(',')
		return None
		
	def getScenariosList(self):
		"""METHOD TITestListParser.getScenariosList
	
	Input: None
	Output: None"""
		return self.scenariosListAuto, self.scenariosListManual

	def setPrefix(self):
		"""METHOD TITestListParser.setPrefix
	
	Input: None
	Output: None"""
		self.prefix = self.drivers.getKeyValue(self.driver, 'prefix')
		return None
	
	def getPrefix(self):
		"""METHOD TITestListParser.getPrefix
	
	Input: None
	Output: None"""
		return self.prefix

	def setBuiltScenariosList(self):
		"""METHOD TITestListParser.setBuiltScenariosList
	
	Input: None
	Output: None"""
		self.builtScenariosList = []
		tempPrefix = self.getPrefix()
		for eachscenario in self.scenariosList:
			newScenario = tempPrefix + eachscenario
			self.builtScenariosList.append(newScenario)
		return None
		
	def getBuiltScenariosList(self):
		"""METHOD TITestListParser.getBuiltScenariosList
	
	Input: None
	Output: None"""
		return self.builtScenariosList
