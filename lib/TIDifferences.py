#!/usr/bin/python

# ===============================================================
# CLASS: TIDifferences
# ===============================================================

Version = '0.01'

import os
import sys
import commands
import tempfile
import TIMessage

from TIUtilities import *

class TIDifferences:
	def __init__(self, primaryPath = None, secondaryPath = None):
		
		self.message = TIMessage.TIMessage(True)
		self.primaryPath = primaryPath
		self.secondaryPath = secondaryPath
		self.differencesFileName = None
		self.diffstatFileName = None
		self.tempFile = None
		
		self.message.INFO('Getting Differences')
		self.differencesFileName = self.createTemporalFile()
		self.setDifferencesFileName(self.differencesFileName)
		self.getDifferences()
	
		self.message.INFO('Getting Diffstat information')
		self.diffstatFileName = self.createTemporalFile()
		self.setDiffstatFileName(self.diffstatFileName)
		self.getDiffstat()
		
		return None
	
	def createTemporalFile(self):
		"""METHOD Differences.createTemporalFile
	Create a temporal file
	Input: None
	Output: None"""
		self.tempFile = tempfile.mktemp()
		logfile = open(self.tempFile, "w+b")
		os.chmod(self.tempFile , 0777)
		return self.tempFile
		
	def deleteTemporalFile(self, fd):
		"""METHOD Differences.deleteTemporalFile
	Delete a temporal file
	Input: None
	Output: None"""
		os.remove(fd)
		return None

	def setDifferencesFileName(self, differencesFileName):
		"""METHOD Differences.setDifferencesFileName
	Set the name for the differences file
	Input: differencesFileName
	Output: None"""
		self.differencesFileName = differencesFileName
		return None

	def getDifferencesFileName(self):
		"""METHOD Differences.getDifferencesFileName
	Get the name of the differences file
	Input: None
	Output: differencesFileName"""
		return self.differencesFileName

	def setDiffstatFileName(self, diffstatFileName):
		"""METHOD Differences.setDiffstatFileName
	Set the name for the diffstat file
	Input: diffstatName
	Output: None"""
		self.diffstatFileName = diffstatFileName
		return None

	def getDiffstatFileName(self):
		"""METHOD Differences.getDiffstatFileName
	Get the name of the diffstat file
	Input: None
	Output: diffstatFileName"""
		return self.diffstatFileName

	def setPrimaryPath(self, primaryPath):
		"""METHOD Differences.setPrimaryPath
	Set the primary path
	Input: primaryPath
	Output: None"""
		self.primaryPath = primaryPath
		return None
	
	def getPrimaryPath(self):
		"""METHOD Differences.getPrimaryPath
	Get the primary path
	Input: None
	Output: primaryPath"""
		return self.primaryPath
		
	def setSecondaryPath(self, secondaryPath):
		"""METHOD Differences.setSecondaryPath
	Set the secondary path
	Input: secondaryPath
	Output: None"""
		self.secondaryPath = secondaryPath
		return None
	
	def getSecondaryPath(self):
		"""METHOD Differences.getSecondaryPath
	Get the secondary path
	Input: None
	Output: secondaryPath"""
		return self.secondaryPath

	def cleanUpDirectory(self):
		"""METHOD Differences.cleanUpDirectory
	Clean up the current directory
	Input: None
	Output: None"""	
		cmd = 'make distclean'
		status, output = commands.getstatusoutput(cmd)
		if status:
			self.message.ERROR('Error cleaning directory')
		return status, output		
		
	def getDiffstat(self):
		"""METHOD Differences.getDiffstat
	Get the diffstat of the differences filename
	Input: None
	Output: None"""	
		cmd = ('diffstat %s > %s' % \
					(self.differencesFileName, self.diffstatFileName))
		self.message.INFO(cmd)					
		status, output = commands.getstatusoutput(cmd)
		if status:
			self.message.ERROR('Error getting diffstat -> Status %s' % status)
		return status, output	
		
	def getDifferences(self):
		"""METHOD Differences.getDifferences
	Get the differences between primary and secondary path
	Input: None
	Output: None"""	
		
		cmd = ('diff -purN %s %s > %s' % \
					(self.primaryPath, self.secondaryPath, self.differencesFileName))
		self.message.INFO(cmd)
		status, output = commands.getstatusoutput(cmd)
		if status == 0:
			self.message.INFO('No differences found')
		elif status == 256:
			self.message.INFO('Differences found')
		else:
			self.message.ERROR('Error getting differences -> Status %s' % status)
		return status, output
