#!/usr/bin/python

# ===============================================================
# CLASS: TICopyManager
# ===============================================================

import os
import re
import sys
import time
import shutil
import commands
import TIMessage
import TISettingsManager

class TICopyManager:

	class __impl:
		""" Implementation of the singleton interface """
		
		def spam(self):
			""" Test method, return singleton id """
			return id(self)

	__instance = None

	def __init__(self, release = None, board = None, directory = None):
		
		if TICopyManager.__instance is None:
			# Create and remember instance
			TICopyManager.__instance = TICopyManager.__impl()
	
			self.message = TIMessage.TIMessage(True)
			
			self.release = release
			self.board = board
			self.directoryName = directory
		
			self.message = TIMessage.TIMessage(True)
			self.settings = TISettingsManager.TISettingsManager()
			
			self.repository = None
			self.moduleName = None
			self.kernelId =  None
			self.currentDir = None
			self.nightlyBuildDir = None
			
			self.setKernelId()
			self.createDirectory()
			
		self.__dict__['_TICopyManager__instance'] = TICopyManager.__instance
		
		return None
		
	def __getattr__(self, attr):
		""" Delegate access to implementation """
		return getattr(self.__instance, attr)

	def __setattr__(self, attr, value):
		""" Delegate access to implementation """
		return setattr(self.__instance, attr, value)

	def backUpFiles(self):
		"""METHOD TICopyManager.createDirectory
	Create the directory
	Input: None
	Output: None"""
		print 'I am backing up files'
		return None

	def createDirectory(self):
		"""METHOD TICopyManager.createDirectory
	Create the directory
	Input: None
	Output: None"""
		self.nightlyBuildDir = self.settings.getKeyValue('repository.nightlybuilds')
		for file in os.listdir(self.nightlyBuildDir):
			if (time.time() - os.stat(self.nightlyBuildDir + '/' + file)[-2]) > (7 * 24 * 60 * 60):
				if os.path.isdir(file):
					print 'Cleaning Up : %s' % file
		self.currentDir = os.path.join(self.nightlyBuildDir, self.directoryName)
		if not os.path.exists(self.currentDir):
			os.makedirs(self.currentDir,0777)	
		return None

	def setModuleName(self, moduleName):
		"""METHOD TICopyManager.setModuleName
	Set the name of the module
	Input: None
	Output: None"""	
		self.moduleName = moduleName
		return None

	def setKernelId(self):
		"""METHOD TICompile.setKernelId
	Set Kernel Id
	Input: None
	Output: None"""
		self.kernelId = '%s.%s.%s' % (self.release, self.board, 'default')
		return None

	def startTransfer(self):
		"""METHOD TICompile.startTransfer
	Copy output files
	Input: None
	Output: None"""
	
		outputFiles = {'x-load': ['x-load.bin', 'warnings.x-load'],
				'u-boot': ['u-boot.bin', 'tools/mkimage', 'warnings.u-boot'],
				'kernel': ['arch/arm/boot/uImage', \
				'warnings.defconfig', \
				'warnings.uImage', \
				'warnings.modules', \
				'warnings.uImage.only']}
		
		for counter in range (0, len(outputFiles[self.moduleName])):
		
			fileName = outputFiles[self.moduleName][counter]
						
			if re.match('warnings', fileName):
				
				self.repository = self.settings.getKeyValue('repository.warnings')
				if self.moduleName == 'kernel':
					name = '%s.%s' % (self.kernelId, fileName)
				else:
					name = '%s.%s.%s' % (self.release, self.board , fileName)
				shutil.copy(fileName, '%s/%s' % (self.repository, name))
				shutil.copy(fileName, '%s/%s' % (self.currentDir, name))
				
			elif re.match('x-load.bin', fileName):
			
				self.repository = self.settings.getKeyValue('repository.x-load')
				name = '%s.%s.%s' % (fileName, self.release, self.board)
				shutil.copy(fileName, '%s/%s' % (self.repository, name))
				shutil.copy(fileName, '%s/%s' % (self.currentDir, name))

			elif re.match('u-boot.bin', fileName):
			
				self.repository = self.settings.getKeyValue('repository.u-boot')
				name = '%s.%s.%s' % (fileName, self.release, self.board)
				shutil.copy(fileName, '%s/%s' % (self.repository, name))
				shutil.copy(fileName, '%s/%s' % (self.currentDir, name))				

			elif re.match('tools', fileName):
			
				self.repository = self.settings.getKeyValue('exported.directory')
				name = '%s/mkimage' % self.repository
				shutil.copy(fileName, name)
			
			elif re.match('arch', fileName):
			
				self.repository = self.settings.getKeyValue('repository.kernel')
				name = 'uImage.%s' % self.kernelId
				shutil.copy(fileName, '%s/%s' % (self.repository, name))
				shutil.copy(fileName, '%s/%s' % (self.currentDir, name))
				self.repository = '%s/%s' % (self.settings.getKeyValue('repository.testsuites'), 'modules')
				if os.path.exists(self.repository):
					shutil.rmtree(self.repository)
				os.makedirs(self.repository, 0777)
				file = open('warnings.modules', 'r')
				for line in file:
					templine = re.sub(r"\s*", '', line)
					if re.match(r"LD\[M\]?", templine):
	 					modulePath = re.sub(r"LD\[M\]?", '', templine)
	 					shutil.copy(modulePath, self.repository)
				file.close()
				
		return None
