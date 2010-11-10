#!/usr/bin/python

# ===============================================================
# CLASS: TIClearCaseView
# ===============================================================

Version = '0.01'

import os
import sys
import commands
import TIMessage

class TIClearCaseView:
	def __init__(self, userName = None, suffix = None, configSpecPath = None):
		
		
		self.configSpecPath = configSpecPath
		self.userName = userName
		self.suffix = suffix
		self.name = 'None'
		self.rawPath = 'None'
		self.viewName = 'None'

		self.message = TIMessage.TIMessage(True)

		self.setViewName()
		#self.mkViewLinked()
		self.setPath()
		self.startView()

		return None

	def setConfigSpecPath(self, configSpecPath):
		"""METHOD ClearCaseView.setConfigSpecPath
	Set config spec path
	Input: configSpecPath
	Output: None"""
		if os.path.exists(configSpecPath):
			self.configSpecPath = configSpecPath
		else:
			self.message.ERROR('Requested path is not available %s' % configSpecPath)
		return None
	
	def getConfigSpecPath(self):
		"""METHOD ClearCaseView.getConfigSpecPath
	Get config spec path
	Input: None
	Output: configSpecPath"""
		return self.configSpecPath
	
	def setUserName(self, userName):
		"""METHOD ClearCaseView.setUserName
	Set username for view creation
	Input: userName
	Output: None"""
		self.userName = userName
		return None

	def getUserName(self):
		"""METHOD ClearCaseView.getUserName
	Get user name
	Input: None
	Output: userName"""
		return self.userName
	
	def setSuffix(self):
		"""METHOD ClearCaseView.setSuffix
	Set suffix for view creation
	Input: suffix
	Output: None"""
		self.suffix = suffix
		return None
	
	def getSuffix(self):
		"""METHOD ClearCaseView.getSuffix
	Get suffix
	Input: None
	Output: suffix"""
		return self.suffix

	def setViewName(self):
		"""METHOD ClearCaseView.setViewName
	Set ClearCase view name
	Input: None
	Output: None"""
		self.viewName = 'omapsw_%s_%s' % (self.userName, self.suffix)
		return None

	def getViewName(self):
		"""METHOD ClearCaseView.getViewName
	Get ClearCase view name
	Input: None
	Output: viewName"""
		return self.viewName

	def setPath(self):
		"""METHOD ClearCaseView.setPath
	Set path /view/...
	Input: None
	Output: None"""
		self.path = '/view/%s' % self.viewName
		return None
	
	def getPath(self):
		"""METHOD ClearCaseView.getPath
	Get path
	Input: None
	Output: path"""
		return self.path
	
	def setConfigSpec(self):
		"""METHOD ClearCaseView.setConfigSpec
	Set config spec to current view from a file
	Input: None
	Output: status, output"""
		cmd = '/usr/atria/bin/cleartool setcs -tag %s %s' % \
					(self.viewName, self.configSpecPath)
		status, output = commands.getstatusoutput(cmd)
		if status:
			self.message.ERROR('Error setting config spec: %s' % cmd)
		return status, output

	def catConfigSpec(self):
		"""METHOD ClearCaseView.catConfigSpec
	Cat config spec
	Input: None
	Output: status, output"""
		cmd = '/usr/atria/bin/cleartool catcs'
		status, output = commands.getstatusoutput(cmd)
		if status:
			self.message.ERROR('Error setting config spec: %s' % cmd)
		return status, output		
		
		
	def startView(self):
		"""METHOD ClearCaseView.startView
	Start View
	Input: None
	Output: status, output"""
		cmd = '/usr/atria/bin/cleartool startview %s' % self.viewName
		status, output = commands.getstatusoutput(cmd)
		if status:
			self.message.ERROR('Error starting view: %s' % cmd)
		return status, output
		
	def endView(self):
		"""METHOD ClearCaseView.endView
	End View
	Input: None
	Output: status, output"""
		cmd = '/usr/atria/bin/cleartool endview %s' % \
					(self.viewName)
		status, output = commands.getstatusoutput(cmd)
		if status:
			self.message.ERROR('Error ending view: %s' % cmd)
		return status, output		
		
	def mkViewLinked(self):
		"""METHOD ClearCaseView.mkViewLinked
	Create a ClearCase view
	Input: None
	Output: status, output"""
		cmd = '/usr/local/bin/mkview_linked %s' % self.viewName
		status, output = commands.getstatusoutput(cmd)
		if status:
			self.message.ERROR('Error creating view: %s' % cmd)
		return status, output
	
	def rmView(self):
		"""METHOD ClearCaseView.rmView
	Delete a ClearCase view
	Input: None
	Output: status, output"""
		cmd = '/usr/atria/bin/cleartool rmview -tag %s' % self.viewName
		status, output = commands.getstatusoutput(cmd)
		if status:
			self.message.ERROR('Error deleting view: %s' % cmd)
		return status, output
