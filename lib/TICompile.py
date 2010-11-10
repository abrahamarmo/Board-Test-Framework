#!/usr/bin/python

# ===============================================================
# CLASS: TICompile
# ===============================================================

import os
import re
import sys
import time
import commands

import TIMessage
import TIReleaseManager
import TISettingsManager
import TIDriverManager

class Error(Exception):
    """Base class for Compile exceptions."""
    def __init__(self, msg=''):
        self.message = msg
        Exception.__init__(self, msg)

    def __repr__(self):
        return self.message

    __str__ = __repr__

"""    
class NoModuleNameError(Error):
    def __init__(self, moduleName):
        Error.__init__(self, 'No module name: %r' % (moduleName,))
        self.moduleName = moduleName
"""

class NoModulePathError(Error):
    """Raised when no module path exists"""
    def __init__(self, modulePath):
        Error.__init__(self, 'No module path: %r' % (modulePath,))
        self.modulePath = modulePath

class CleanUpError(Error):
    """Raised when clean up error happens"""
    def __init__(self):
        Error.__init__(self, 'Clean Up Compilation Error')
        
        
class XloadCompilationError(Error):
    """Raised when x-load compilation error happens"""
    def __init__(self):
        Error.__init__(self, 'X-load Compilation Error')

class UbootCompilationError(Error):
    """Raised when u-boot compilation error happens"""
    def __init__(self):
        Error.__init__(self, 'U-boot Compilation Error')
        
class KernelCompilationError(Error):
    """Raised when kernel compilation error happens"""
    def __init__(self):
        Error.__init__(self, 'Kernel Compilation Error')        

        
class TestSuiteCompilationError(Error):
    """Raised when testsuites compilation happens"""
    def __init__(self):
        Error.__init__(self, 'Test Suite Compilation Error')

class TICompile:

	def __init__(self, mainRelease = None, \
		release = None, \
		board = None, \
		module = None, \
		defconfigPath = None):

		self.mainRelease=mainRelease
		self.release=release
		self.board=board
		self.platformName = self.mainRelease+self.board
		self.moduleName = module
		self.defconfigPath = defconfigPath
		
		self.kernelId = None
		
		self.modulePath = None
		self.compilationSteps = None
		self.defconfigName = None
		
		self.message = TIMessage.TIMessage(True)
		self.drivers = TIDriverManager.TIDriverManager()
		self.settings = TISettingsManager.TISettingsManager()
		
		self.releases = TIReleaseManager.TIReleaseManager(self.platformName)
		self.releases.setCrossCompilerPrefix()
		self.crossCompiler = 'CROSS_COMPILE=%s' % self.releases.getCrossCompilerPrefix()
		self.releases.setHostPrefix()
		self.host = 'HOST=%s' % self.releases.getCrossCompilerPrefix()
		
		self.compile()
		
		return None

	def removeNonWarnings(self):
		"""METHOD TICompile.removeNonWarnings
	Remove Non warnings
	Input: None
	Output: None"""
		myfile = open('warnings.uImage', 'r')
		fileList = myfile.readlines()
		warnings = []
		for lineStr in fileList:
			lineStr = lineStr.replace('/n', '')
			if lineStr[0] != ' ':
				warnings.append(lineStr)
				lineStr = myfile.readline()
		outfile = open('warnings.uImage.only', 'w')
		outfile.writelines(warnings)
		outfile.close()
		myfile.close()
		return None

	def applyDefconfig(self, defconfigName):
		"""METHOD TICompile.applyDefconfig
	Apply defconfig path
	Input: None
	Output: None"""
		self.message.INFO('Applying defconfig')
		cmd = 'cp %s/%s %s/.config' % (self.defconfigPath, defconfigName, self.modulePath)
		self.message.INFO(cmd)
		status, output = commands.getstatusoutput(cmd)
		if status:
			self.message.ERROR('Error copying defconfig file')
		return status, output
		
	def getDefconfigList(self):
		"""METHOD TICompile.getDefconfigList
	get defconfig list
	Input: None
	Output: None"""
		return self.defconfigList

	def setDefConfigName(self, defconfigName):
		"""METHOD TICompile.setDefConfigName
	Set defconfig name 
	Input: defconfigName
	Output: None"""
		self.defconfigName = defconfigName
		return None

	def getDefConfigName(self):
		"""METHOD TICompile.getDefConfigName
	Get defconfig name
	Input: None
	Output: defconfigName"""
		return self.defconfigName
		
	def setModulePath(self):
		"""METHOD TICompile.setModulePath
	Set module path
	Input: modulePath
	Output: None"""
		
		if self.settings.getKeyValue('local.compilation?') == 'y':
			self.modulePath = self.settings.getKeyValue('local.'+self.moduleName+'.path')
		else:
			self.modulePath = self.releases.getKeyValue(self.moduleName+'path')
			if self.moduleName == 'testsuites':
				self.modulePath = os.path.join('/view/%s/%s' %\
				(self.settings.getKeyValue('framework.view'),\
				self.settings.getKeyValue('main.testsuites')))
		if not os.path.exists(self.modulePath):
			self.message.FATAL('Module path does not exist > %s' % self.modulePath)
			raise NoModulePathError(self.modulePath)
		self.message.INFO('Setting %s path to %s' % (self.moduleName, self.modulePath))
		os.chdir(self.modulePath)
		return None

	def getModulePath(self):
		"""METHOD TICompile.getModulePath
	Get module path
	Input: None
	Output: modulePath"""
		return self.modulePath
		
	def cleanUpDirectory(self, cmd):
		"""METHOD TICompile.cleanUpDirectory
	Clean Up Directory
	Input: None
	Output: None"""
		cmd = 'make %s %s' % (self.crossCompiler, cmd)
		self.message.INFO(cmd)
		status, output = commands.getstatusoutput(cmd)
		if status:
			self.message.ERROR('Error cleaning directory')
			raise CleanUpError()
		return status, output

	def parseModulesList(self):
		validModules = ['x-load', 'u-boot', 'kernel', 'testsuites', 'filesystem']
		for x in self.modules:
			try:
				validModules.index(x)
				self.modulesList.append(x)
			except ValueError:
				self.message.FATAL('No module found with name %s' % x)
				self.message.FATAL('Valid module names : %s' % validModules)
				raise NoModuleNameError(x)
		return None

	def outputFileToScreen(self, afile, lines=0):
		self.message.ERROR('')
		counter = 0
		f = file(afile)
		all_lines = f.readlines()
		lines_in_total = len(all_lines)
		for line in all_lines:
			counter = counter + 1
			if lines == 'all':
				self.message.ERROR('\t'+line.strip('\n'))		
			else:
				if counter >= lines_in_total-lines:
					self.message.ERROR('\t'+line.strip('\n'))
		self.message.ERROR('')				
		f.close()
		return None	

	def compile(self):
		"""METHOD TICompile.compile
	Compile
	Input: None
	Output: None"""

		self.releases.setModuleName(self.moduleName)
			
		self.moduleName = self.releases.getModuleName()
		self.compilationSteps = self.releases.getCompilationSteps() 
		self.modulePath = self.releases.getModulePath()
		self.defconfigName = self.releases.getDefconfigName()
			
		self.message.INFO('')
		
		os.chdir(self.modulePath)
			
		if self.moduleName == 'x-load':
			self.compileXload()
			
		elif self.moduleName == 'u-boot':
			self.compileUboot()
			
		elif self.moduleName == 'kernel':
			self.compileKernel()
			self.removeNonWarnings()
	
		elif self.moduleName == 'filesystem':
			print 'filesystem'
			
		else:
			self.compileTestSuites()

		self.verifyOutputFiles()
		
		return None

	def compileXload(self):
		"""METHOD TICompile.compileXload
	Compile Xload
	Input: None
	Output: None"""
		
		for counter in range (0, len(self.compilationSteps)):
			if self.compilationSteps[counter] == 'none':
				cmd = 'make %s &> warnings.%s' % (self.crossCompiler, self.moduleName)
				self.message.INFO(cmd)
				status, output = commands.getstatusoutput(cmd)
				if status:
					self.message.ERROR('Error compiling %s' % self.moduleName)
					self.outputFileToScreen('warnings.%s' % self.moduleName, lines=10)
			elif self.compilationSteps[counter] == 'defconfig':
				cmd = 'make %s %s' % (self.crossCompiler, self.defconfigName)
				self.message.INFO(cmd)
				status, output = commands.getstatusoutput(cmd)
				if status:
					self.message.ERROR('Error setting defconfig')
					raise XloadCompilationError()
			else:
				self.cleanUpDirectory('distclean')
		return None
		
	def compileUboot(self):
		"""METHOD TICompile.compileUboot
	Compile Uboot
	Input: None
	Output: None"""

		for counter in range (0, len(self.compilationSteps)):
			if self.compilationSteps[counter] == 'none':
				cmd = 'make %s &> warnings.%s' % (self.crossCompiler, self.moduleName)
				self.message.INFO(cmd)
				status, output = commands.getstatusoutput(cmd)
				if status:
					self.message.ERROR('Error compiling %s' % self.moduleName)
					self.outputFileToScreen('warnings.%s' % self.moduleName, lines=10)
			elif self.compilationSteps[counter] == 'defconfig':
				cmd = 'make %s %s' % (self.crossCompiler, self.defconfigName)
				self.message.INFO(cmd)
				status, output = commands.getstatusoutput(cmd)
				if status:
					self.message.ERROR('Error setting defconfig')
					raise UbootCompilationError()
			else: 
				self.cleanUpDirectory('distclean')
		return None
	
	def compileKernel(self):
		"""METHOD TICompile.compileKernel
	Compile kernel module
	Input: None
	Output: None"""
		
		for counter in range (0, len(self.compilationSteps)):
			warningsfile = 'warnings.%s' %  self.compilationSteps[counter]
			if self.compilationSteps[counter] != 'distclean':
				step = self.compilationSteps[counter]
				if self.compilationSteps[counter] == 'defconfig':
					step = self.defconfigName
				if self.compilationSteps[counter] != 'defconfig' or self.defconfigName:
					cmd = 'make %s %s &> %s' % (self.crossCompiler, step, warningsfile)
					self.message.INFO(cmd)
					status, output = commands.getstatusoutput(cmd)
					if status:
						self.message.ERROR('Error compiling kernel in %s' % \
						self.compilationSteps[counter])
						self.outputFileToScreen('warnings.%s' % \
						self.compilationSteps[counter], lines=10)
						raise KernelCompilationError()
			else:
				self.cleanUpDirectory('distclean')
		return None

	def compileTestSuites(self):
		"""METHOD TICompile.compileTestSuites
	Compile testsuites
	Input: None
	Output: None"""

		self.drivers 	= TIDriverManager.TIDriverManager()
		
		if self.settings.getKeyValue('local.compilation?') == 'y':
				KDIR = 'KDIR=%s' % self.settings.getKeyValue('local.kernel.path')
		else:
				KDIR = 'KDIR=%s' % self.releases.getKeyValue('kernelpath')

		self.settings.setKeyValue('utils', 'y')
		drivers = self.settings.getAllOptions('drivers')

		for eachdriver in range (0, len(drivers)):
			
			if self.settings.getKeyValue(drivers[eachdriver]) == 'y':
				self.message.INFO('< < < < < < %s > > > > > >' % drivers[eachdriver])
				source = os.path.join(self.modulePath, \
									self.drivers.getKeyValue(drivers[eachdriver],'dirname'))
				if self.settings.getKeyValue('local.compilation?') == 'y':
					source = source.replace('/test_code', '')
				destination = os.path.join(self.settings.getKeyValue('repository.testsuites'), \
				drivers[eachdriver])
				
				if os.path.exists(destination):
					try:
						shutil.rmtree(destination)
					except Error:
						self.message.ERROR('Error deleting directory')
						raise TestsuiteCompilationError()
				
				os.chdir(source)
				self.cleanUpDirectory('clean')
				cmd = 'make %s %s %s' % (self.crossCompiler, self.host, KDIR)
				self.message.INFO(cmd)
				status, output = commands.getstatusoutput(cmd)
				if status:
					self.message.ERROR('Error compiling')
					self.message.ERROR(output)
					raise TestsuiteCompilationError()
				self.message.INFO('Copying to %s' % destination)
				shutil.copytree(source, destination, symlinks=True)
				self.cleanUpDirectory('clean')
				
		return None
		
	def verifyOutputFiles(self):
		"""METHOD TICompile.verifyOutputFiles
	Verify output files
	Input: None
	Output: None"""
		outputFiles = {'x-load': 'x-load.bin',
									'u-boot': 'u-boot.bin',
									'kernel': 'arch/arm/boot/uImage'}
		outputFile = outputFiles[self.moduleName]
		if os.path.exists(outputFile):
			self.message.INFO('')
			self.message.INFO('[%s compilation] SUCCEEDED' % self.moduleName)
		else:
			self.message.INFO('')
			self.message.INFO('[%s compilation] FAILED' % self.moduleName)
			sys.exit(-1)
		return None


"""
def createDefconfigList(self):
		if self.defconfigPath != 'default':
			self.message.INFO('Creating defconfig list')
			self.defconfigList = os.listdir(self.defconfigPath)
		else:
			self.defconfigList.append(self.defconfigPath)
		return None
"""

"""
			print self.getDefconfigList()
			for eachDefconfig in self.getDefconfigList():
				if eachDefconfig != 'default':
					self.applyDefconfig(eachDefconfig)
				else:
					self.defconfigName= self.releases.getKeyValue(self.moduleName+'DefConfig')
				self.setKernelId(eachDefconfig)
				self.compileKernel()
				self.removeNonWarnings()
				#self.copyOutputFiles()
"""
