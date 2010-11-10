#!/usr/bin/python

import os
import sys
import time
import string
import fileinput
import ConfigParser

import TIMessage
import TICompile
import TISettingsManager
import TICopyManager

if __name__ == '__main__':

	releaseinformation =	sys.argv[1]
	mainRelease, release, board = releaseinformation.split(':')
	module	= sys.argv[2]	
	settingsFile = sys.argv[3]
	configSpec = sys.argv[4]
	localCompilation = sys.argv[5]
	testView = sys.argv[6]
	defconfigPath	= sys.argv[7]

	messages  = TIMessage.TIMessage(True)
	settings  = TISettingsManager.TISettingsManager(settingsFile=settingsFile)
	#date = time.strftime("%Y.%m.%d.%A.%H.%M")
	date = time.strftime("%Y.%m.%d.%A")
	copy = TICopyManager.TICopyManager(release, board, date)

	oldValues = os.environ['PATH']
	exportedDirectory = settings.getKeyValue('exported.directory')
	os.environ['PATH'] = '%s:%s' % (oldValues, exportedDirectory)
	oldValues = os.environ['PATH']
	toolchainPath = settings.getKeyValue('tool.chain.path')
	os.environ['PATH'] = '%s:%s' % (oldValues, toolchainPath)
	
	messages.INFO('')

	if localCompilation == 'local':
		messages.INFO('Release %s | Board %s | %s | Local Compilation' % \
			(release, board, module))		
		settings.setKeyValue('local.compilation?', 'y')
	else:
		messages.INFO('Release %s | Board %s | %s | Clear Case Compilation' % \
			(release, board, module))	
		settings.setKeyValue('local.compilation?', 'n')
		settings.setKeyValue('clear.case.view', localCompilation)
		settings.setKeyValue('framework.view', testView)
	
	for line in fileinput.input(configSpec):
		lineno = 0
		lineno = string.find(line, module)
		if lineno > 0:
			lineno = 0
			lineno = string.find(line, 'element')
			if lineno >= 0:
				messages.INFO('')
				messages.INFO('%s' % line.strip())
	
	#try:
	
	compile = TICompile.TICompile(\
			mainRelease=mainRelease,\
			release=release,\
			board=board,\
			module=module,\
			defconfigPath=defconfigPath)
		
	copy.setModuleName(module)
	copy.startTransfer()
	
	#except:
	#	messages.ERROR('Compilation Error')
	#	sys.exit(1)

	messages.INFO('')
