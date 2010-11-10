#!/usr/bin/python

import sys

# ===============================================================
# CLASS: TIMessage
# ===============================================================

class TIMessage:
	def __init__(self, active = True, fileLogging = False):
		self.active = active
		self.logFilename = None
		self.fileLogging = fileLogging
		return

	def setLogFile(self, logFilename):
		self.logFilename = logFilename
		return None
		
	def INFO(self, message):
		if self.active:
			sys.stdout.write('|    INFO | %s\n' % message)
			sys.stdout.flush()
		if self.fileLogging:
			open(self.logFilename, 'at').write('|    INFO | %s\n' % (message))
		return None

	def FAIL(self, message):
		if self.active:
			sys.stdout.write('|    FAIL | %s\n' % message)
			sys.stdout.flush()
		if self.fileLogging:
			open(self.logFilename, 'at').write('|    FAIL | %s\n' % (message))
		return None

	def ERROR(self, message):
		if self.active:
			sys.stdout.write('|   ERROR | %s\n' % message)
			sys.stdout.flush()
		if self.fileLogging:
			open(self.logFilename, 'at').write('|   ERROR | %s\n' % (message))			
		return None
	
	def FATAL(self, message):
		sys.stdout.write('|   FATAL | %s\n' % message)
		sys.stdout.flush()
		if self.fileLogging:
			open(self.logFilename, 'at').write('|   FATAL | %s\n' % (message))		
		return None

	def SUCCESS(self, message):
		sys.stdout.write('| SUCCESS | %s\n' % message)
		sys.stdout.flush()
		if self.fileLogging:
			open(self.logFilename, 'at').write('| SUCCESS | %s\n' % (message))		
		return None
