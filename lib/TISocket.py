#!/usr/bin/python

import socket
import time 
import TIMessage

class TISocket:

	class __impl:
		""" Implementation of the singleton interface """
		def spam(self):
			""" Test method, return singleton id """
			return id(self)

	__instance = None

	def __init__(self, ipaddr = None, port = None):
		if TISocket.__instance is None:
			# Create and remember instance
			TISocket.__instance = TISocket.__impl()
	
			self.message = TIMessage.TIMessage(True)
			self.ipaddr = ipaddr
			self.port = int(port)
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.connect()
		
			self.__dict__['_TISocket__instance'] = TISocket.__instance
		
		return None

	def __getattr__(self, attr):
		""" Delegate access to implementation """
		return getattr(self.__instance, attr)

	def __setattr__(self, attr, value):
		""" Delegate access to implementation """
		return setattr(self.__instance, attr, value)

	def connect(self):
		"""METHOD TISocket.connect
	
	Input: None
	Output: None"""	
		self.sock.connect((self.ipaddr, self.port))
		return None

	def send(self, message, wait):
		"""METHOD TISocket.send
	
	Input: None
	Output: None"""
		self.message.INFO(message)
		messlen, received = self.sock.send(message), 0
		time.sleep(wait)
		return messlen, received

	def close(self):
		"""METHOD TISocket.close
	
	Input: None
	Output: None"""	
		self.sock.close()
		return None
