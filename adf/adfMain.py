#!/usr/bin/python

import os
import sys

import TIMessage
import TIDifferences
import TIReleaseManager
import TISettingsManager
import TIEmail

from TIUtilities import *

if __name__ == '__main__':  


	preleaseinformation	=	sys.argv[1]
	pmainRelease, prelease = preleaseinformation.split(':')
	sreleaseinformation	=	sys.argv[2]
	smainRelease, srelease = sreleaseinformation.split(':')
	module = sys.argv[3]
	settingsFile = sys.argv[4]
	board = sys.argv[5]
	
	message = TIMessage.TIMessage(True)
	settings = TISettingsManager.TISettingsManager(settingsFile)
	release = TIReleaseManager.TIReleaseManager()
	
	userName = settings.getKeyValue('username')
	pplatformName = pmainRelease+board
	splatformName = smainRelease+board

	#----------------------------------------------------------------------------
	# Set the paths for both releases
	#----------------------------------------------------------------------------
	
	release.setPlatformName(pplatformName)
	primaryDirectory = release.getKeyValue(module + 'Path')
	
	release.setPlatformName(splatformName)
	secondaryDirectory = '/view/omapsw_%s_%sdiff' % (userName, srelease) + \
											release.getKeyValue(module + 'Path')	
	
	differences = TIDifferences.TIDifferences(primaryPath = primaryDirectory, \
																						secondaryPath = secondaryDirectory)
	
	#----------------------------------------------------------------------------
	# Copy differences results to repositories
	#----------------------------------------------------------------------------
	
	os.system('cp %s %s/differences.%s.%s' % \
					(differences.getDifferencesFileName(), \
					settings.getKeyValue('repository.differences'), prelease, srelease))
	
	os.system('cp %s %s/diffstat.%s.%s' % \
					(differences.getDiffstatFileName(), \
					settings.getKeyValue('repository.differences'), prelease, srelease))
					
	#----------------------------------------------------------------------------
	# Send email of differences found
	#----------------------------------------------------------------------------

	email = settings.getKeyValue('email')
	subject = '[Linux Baseport] [Differences] [%s] %s %s' % (module, prelease, srelease)
	attachmentPath = toZip(differences.getDifferencesFileName(), \
													"differences.zip", \
													File=True)

	email = TIEmail.TIEmail(email=email, subject=subject, \
													body=differences.getDiffstatFileName(), \
													attachmentPath=attachmentPath)
	
	email.sendEmailwithMutt()
	
	#----------------------------------------------------------------------------
	# Differences file was created, do clean up removing it
	#----------------------------------------------------------------------------

	os.remove('differences.zip')

		
