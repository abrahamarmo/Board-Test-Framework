#!/usr/bin/python

import os
import commands
import TIMessage

class TIEmail:

	class __impl:
		""" Implementation of the singleton interface """
		def spam(self):
			""" Test method, return singleton id """
			return id(self)

	__instance = None

	def __init__(self, email = None, subject = None, body = None, attachmentPath = None):
		if TIEmail.__instance is None:
			# Create and remember instance
			TIEmail.__instance = TIEmail.__impl()
	
			self.message = TIMessage.TIMessage(True)
			self.email = email
			self.subject = subject
			self.body = body
			self.attachmentPath = attachmentPath
			
			self.__dict__['_TIEmail__instance'] = TIEmail.__instance
			
		return None

	def setEmailAddress(self, email):
		"""METHOD Differences.setEmailAddress
	Set email address
	Input: userName
	Output: None"""
		self.email = email
		return None

	def setSubject(self, subject):
		"""METHOD TIEmail.setSubject
	Set subject 
	Input: None
	Output: None"""
		self.subject = subject
		return None
		
	def setBody(self, body):
		"""METHOD TIEmail.setBody
	set body content
	Input: None
	Output: None"""
		self.body = body
		return None

	def setAttachmentPath(self, path):
		"""METHOD Differences.setAttachmentPath
	Set attachment path
	Input: path
	Output: None"""
		self.attachmentPath = path
		return None		

	def sendEmailwithMail(self):
		"""METHOD TIEmail.sendEmailwithMail
	Send the email using mail command
	Input: None
	Output: None"""
		self.message.INFO('Sending email')
		cmd = 'cat %s | mail -s "%s" %s' % (self.body, \
																			self.subject, \
																			self.email)
		self.message.INFO(cmd)
		status, output = commands.getstatusoutput(cmd)
		if status:
			self.message.ERROR('Cannot send email')
		return status, output
		
	def sendEmailwithMutt(self):
		"""METHOD TIEmail.sendEmailwithMutt
	Send the email using Mutt command
	Input: None
	Output: None"""
		self.message.INFO('Sending email')
		if not self.attachmentPath:
			cmd = 'mutt -s "%s" %s < %s' % (self.subject, self.email, self.body)
		else:
			cmd = 'mutt -a %s -s "%s" %s < %s' % (self.attachmentPath, \
																						self.subject, \
																						self.email, \
																						self.body)
		self.message.INFO(cmd)																						
		status, output = commands.getstatusoutput(cmd)
		if status:
			self.message.ERROR('Cannot send email')
		return status, output

	
