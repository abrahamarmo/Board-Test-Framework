#!/usr/bin/env python

import os
import sys
import time
import commands
import shutil

import TIEmail
import TIMessage
import TICompile
import TIDriverManager
import TISettingsManager
import TIReleaseManager
import TIReport
import TIBoard
import TISocket
import TITestListParser

from time import gmtime, strftime
	
if __name__ == '__main__':

	releaseinformation = sys.argv[1]
	mainRelease, release, board = releaseinformation.split(':')
	testType = sys.argv[2]
	userfile = sys.argv[3]
	configspec = sys.argv[4]
	
	platformName = mainRelease+board
	
	report = TIReport.TIReport()
	messages = TIMessage.TIMessage(active = True, fileLogging = True)
	settings = TISettingsManager.TISettingsManager(settingsFile = userfile)
	releases = TIReleaseManager.TIReleaseManager(platformName)
	drivers = TIDriverManager.TIDriverManager()
		
	#----------------------------------------------------------------------------
	# Create test results directory | copy test list file to testresults repo
	#----------------------------------------------------------------------------
	
	testResults = '%s.%s.%s' % (platformName, 
															testType,	
															strftime("d%Y%m%d.t%H%M", time.localtime()))
	settings.setKeyValue('testResults', testResults)
	repositoryTestResults = settings.getKeyValue('repository.testresults')
	testResultsDirectory = os.path.join(repositoryTestResults, testResults)
	if not os.path.exists(testResultsDirectory):
		os.makedirs(testResultsDirectory,0777)

	#----------------------------------------------------------------------------
	# Create log file under test results repository
	#----------------------------------------------------------------------------
	
	logFile = testResultsDirectory + '/log.file.txt'
	messages.setLogFile(logFilename = logFile)
	
	messages.INFO('Creating Test Results repository')
	messages.INFO(testResultsDirectory)


	#----------------------------------------------------------------------------
	# Create test list file
	#----------------------------------------------------------------------------
	
	testlist = TITestListParser.TITestListParser(testTypeRequest = testType)
	tempFile = testlist.getTemporalFile()
	shutil.copy(tempFile, testResultsDirectory+'/test.list.sh')
	messages.INFO('Creating Test List script')
	messages.INFO(testResultsDirectory+'/test.list.sh')
	
	#----------------------------------------------------------------------------
	# Create a list for the modules needed to be tested
	#----------------------------------------------------------------------------
 
	tempModulesList = ['x-load', 'u-boot', 'kernel', 'testsuites']
	tempModulesList2Test = []

	for t in tempModulesList:
		if settings.getKeyValue('compile.%s?' % t) == 'y':
			tempModulesList2Test.append(t)

	#----------------------------------------------------------------------------
	# Find out if we need to compile locally or using Clear Case
	#----------------------------------------------------------------------------
	 
	if settings.getKeyValue('local.compilation?') == 'y':
		compileFrom = 'local'
	else:
		compileFrom = settings.getKeyValue('clear.case.view')

	if len(tempModulesList2Test):

		#--------------------------------------------------------------------------
		# There are modules to compile
		# If User is requesting a specific config spec, add it to options
		#--------------------------------------------------------------------------
	
		if configspec != 'None':
			configspec = '-c %s' % configspec
		else: 
			configspec = ''
			
		#--------------------------------------------------------------------------
		# Compile with all settings
		#--------------------------------------------------------------------------		
		messages.INFO('Compilation just begins : %s' % tempModulesList2Test)
		os.chdir('../acf')
		cmd = './acfRun.sh -r %s:%s -m %s -v %s -s %s %s' % (release, \
								board, \
								':'.join(tempModulesList2Test), \
								compileFrom, \
								userfile, \
								configspec)
		status, output = commands.getstatusoutput(cmd)
		if status:
			messages.ERROR('Error in compilation module')
			messages.ERROR(output)
			sys.exit(1)
		messages.INFO(output)
	else:
		messages.INFO('None module to compile')

	#----------------------------------------------------------------------------
	# Inform our framework the needed uImage
	#----------------------------------------------------------------------------

	if settings.getKeyValue('load.this.uimage') == '':
		settings.setKeyValue('load.this.uimage', 'uImage.%s.%s.default' % (release, \
													board))
	
	messages.INFO('Setting uImage to %s' % settings.getKeyValue('load.this.uimage')) 												

	#----------------------------------------------------------------------------
	# Boot up the board
	#----------------------------------------------------------------------------
													
	messages.INFO('Booting the board')
									
	boards 	 = TIBoard.TIBoard( testType = testType )
	
	#----------------------------------------------------------------------------
	# Email Section
	#----------------------------------------------------------------------------

	email = settings.getKeyValue('email')
	subject = '[Linux Baseport] [Test List] %s %s %s' % (release, board, testType)
	
	email = TIEmail.TIEmail(email=email, subject=subject, \
				body=logFile, \
				attachmentPath=tempFile)
	
	email.sendEmailwithMutt()
