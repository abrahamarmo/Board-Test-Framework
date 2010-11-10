#!/usr/bin/python

import os
import sys
import time
import commands
import TIMessage
import TISettingsManager
import TISocket

from time import gmtime, strftime

class TIBoard:
	def __init__(self, testType):
		
		self.message = TIMessage.TIMessage(True)
		self.settings = TISettingsManager.TISettingsManager()
		
		self.message.INFO('')
		
		self.sendOpenTCPSerialConnection()
		
		self.testType = testType
		self.gatewayip = None
		self.ipaddr = None
		self.netmask = None
		self.serverip = None
		self.ethaddr = None
		self.bootargs = None
		self.ubootflashaddress = None
		self.kernelloadaddress = None
		self.nfsuboot = None		
		self.nfsroot = None
		self.nfskernel = None
		self.nfsramdisk = None
		self.nfstestsuites = None
		self.nfstestresults = None

		self.setEthaddr()
		self.setGateway()
		self.setIpaddr()
		self.setNetmask()
		self.setServerip()
		self.setUbootFlashAddress()		
		self.setKernelLoadAddress()
		self.setRamDiskLoadAddress()
		
		self.setNfsKernel()
		self.setNfsRamDisk()
		self.setNfsRoot()
		self.setNfsTestResults()
		self.setNfsTestSuites()		
		
		self.setBootargs()
		self.saveenv()
		self.flashUboot()
		
		self.setRamDiskLoadCommand()
		self.setKernelLoadCommand()
		self.boot()
		self.shellCommands()
		self.closeOpenTCPSerialConnection()

		return None
		
	def reset(self):
		"""METHOD TIBoard.setGateway
	Reset the board
	Input: None
	Output: None"""
		messlen, received = self.socket.send('reset\r', 5)		
		return None

	def saveenv(self):
		"""METHOD TIBoard.setGateway
	Save environment variables
	Input: None
	Output: None"""
		messlen, received = self.socket.send('saveenv\r', 5)		
		return None

	def boot(self):
		"""METHOD TIBoard.boot
	Boot the board
	Input: None
	Output: None"""
		messlen, received = self.socket.send('bootm\r', 25)		
		return None
		
	def flashUboot(self):
		"""METHOD TIBoard.flashUboot
	Flash u-boot
	Input: None
	Output: None"""
		if self.settings.getKeyValue('flash.uboot?') == 'y':
			loadAddress = self.settings.getKeyValue('u-boot.flash.address')
			cmd = self.settings.getKeyValue('u-boot.load.command')
			cmd = cmd.replace('<u-boot>', 'u-boot.bin.12x.2430')
			self.socket.send(cmd, 5)
			#self.socket.send('protect off 1:0-1\r', 2)
			#self.socket.send('erase 1:0-1\r', 2)
			#self.socket.send('cp.b 80000000 %s 2ffff\r' % loadAddress)
			return None
			#cmd = cmd.replace('<u-bootloadadress>', self.u-bootloadaddress)
	    #flashArgs.append('tftpboot 0x80000000 %su-boot.bin.%s.%s\r' %(getColumnValue(uGet, 'nfsuboot', 1), uGet['release'], uGet['board']))
	    #flashArgs.append('protect off 1:0-1\r')
	    #flashArgs.append('erase 1:0-1\r')
	    #flashArgs.append('cp.b 80000000 %s 2ffff\r' % (uGet['ubootflashaddress']))
	    #flashArgs.append('reset\r')
				

	def setPlatform(self):
		"""METHOD TIBoard.setPlatform
	Set platform
	Input: None
	Output: None"""
		return None

	def getPlatform(self):
		"""METHOD TIBoard.getPlatform
	Get platform
	Input: None
	Output: None"""
		return None
		
	def setGateway(self):
		"""METHOD TIBoard.setGateway
	Set gateway
	Input: None
	Output: None"""
		self.gatewayip = self.settings.getKeyValue('gatewayip')
		self.socket.send('setenv gatewayip ' + self.gatewayip+'\r', 1)
		return None

	def setIpaddr(self):
		"""METHOD TIBoard.setenvIpaddress
	Set ipaddr
	Input: None
	Output: None"""
		self.ipaddr = self.settings.getKeyValue('ipaddr')
		self.socket.send('setenv ipaddr ' + self.ipaddr+'\r', 1)		
		return None		

	def setNetmask(self):
		"""METHOD TIBoard.setNetmask
	Set netmask
	Input: None
	Output: None"""
		self.netmask = self.settings.getKeyValue('netmask')
		self.socket.send('setenv netmask ' + self.netmask+'\r', 1)
		return None						

	def setServerip(self):
		"""METHOD TIBoard.setServerip
	Set server ip
	Input: None
	Output: None"""
		self.serverip = self.settings.getKeyValue('serverip')
		self.socket.send('setenv serverip ' + self.serverip+'\r', 1)
		return None
	
	def setEthaddr(self):
		"""METHOD TIBoard.setEthaddr
	Set MAC address
	Input: None
	Output: None"""
		self.ethaddr = self.settings.getKeyValue('ethaddr')
		self.socket.send('setenv ethaddr ' + self.ethaddr+'\r', 1)
		return None

	def setUbootFlashAddress(self):
		"""METHOD TIBoard.setUbootFlashAddress
	Set the adress where u-boot shall be flashed
	Input: None
	Output: None"""
		self.ubootflashaddress = self.settings.getKeyValue('u-boot.flash.address')
		return None				
		
	def setKernelLoadAddress(self):
		"""METHOD TIBoard.setKernelLoadAddress
	Set the adress where kernel shall be loaded
	Input: None
	Output: None"""
		self.kernelloadaddress = self.settings.getKeyValue('kernel.load.address')
		return None

	def setRamDiskLoadAddress(self):
		"""METHOD TIBoard.setRamDiskLoadAddress
	Set the adress where ramdisk shall be loaded
	Input: None
	Output: None"""
		self.ramdiskloadaddress = self.settings.getKeyValue('ramdisk.load.address')
		return None		
	
	def setBootargs(self):
		"""METHOD TIBoard.setBootargs
	Set bootargs
	Input: None
	Output: None"""
		if self.testType == 'auto' or self.testType == 'manual':
			self.bootargs = self.settings.getKeyValue('nfs.fs')
			self.bootargs = self.bootargs.replace('<nfsroot>', self.nfsroot)
			self.bootargs = self.bootargs.replace('<ipaddr>', self.ipaddr)
			self.socket.send('setenv bootargs ' + self.bootargs+'\r', 1)
		else:
			self.bootargs = self.settings.getKeyValue('ramdisk.fs')
			self.bootargs = self.bootargs.replace('<ipaddr>', self.ipaddr)
			self.socket.send('setenv bootargs ' + self.bootargs+'\r', 1)		
		return None

	def setRamDiskLoadCommand(self):
		"""METHOD TIBoard.setRamDiskLoadCommand
	Set the commands to load the ram disk
	Input: None
	Output: None"""
		if self.testType == 'lmbench':
			cmd = self.settings.getKeyValue('ramdisk.load.command')
			cmd = cmd.replace('<ramdiskloadadress>', self.ramdiskloadaddress)
			tempTest = self.nfsramdisk+'/'+self.testType+'.ramdisk'
			cmd = cmd.replace('<ramdisk>', tempTest)+'\r'
			self.socket.send(cmd, 60)
		return None
		
	def setKernelLoadCommand(self):
		"""METHOD TIBoard.setKernelLoadCommand
	Set the commands to load the kernel
	Input: None
	Output: None"""
		cmd = self.settings.getKeyValue('kernel.load.command')
		cmd = cmd.replace('<kernelloadadress>', self.kernelloadaddress)
		uImageName = self.nfskernel+'/'+self.settings.getKeyValue('load.this.uimage')
		cmd = cmd.replace('<kernel>', uImageName)+'\r'
		self.socket.send(cmd, 15)
		return None
	
	def setNfsRoot(self):
		"""METHOD TIBoard.setNfsRoot
	Set nfsroot required in the bootargs
	Input: None
	Output: None"""
		self.nfsroot = self.settings.getKeyValue('nfs.root')
		return None
	
	def getNfsRoot(self):
		"""METHOD TIBoard.getNfsRoot
	Get nfsroot required in the bootargs 
	Input: None
	Output: None"""
		return self.nfsroot
		
	def setNfsKernel(self):
		"""METHOD TIBoard.setKernel
	set path where kernel will be loaded
	Input: None
	Output: None"""
		self.nfskernel = self.settings.getKeyValue('nfs.kernel')
		return None

	def setNfsRamDisk(self):
		"""METHOD TIBoard.setRamDisk
	Set path where ramdisk will be set
	Input: None
	Output: None"""
		self.nfsramdisk = self.settings.getKeyValue('nfs.ramdisk')
		return None
	
	def setNfsUboot(self):
		"""METHOD TIBoard.setNfsUboot
	
	Input: None
	Output: None"""
		self.nfsuboot = self.settings.getKeyValue('nfs.uboot')
		return None		
	
	def getNfsKernel(self):
		"""METHOD TIBoard.getNfsKernel
	
	Input: None
	Output: None"""
		return self.nfskernel

	def setNfsTestSuites(self):
		"""METHOD TIBoard.setNfsTestSuites
	
	Input: None
	Output: None"""
		self.nfstestsuites = self.settings.getKeyValue('nfs.testsuites')
		return None
	
	def getNfsTestSuites(self):
		"""METHOD TIBoard.getNfsTestSuites
	
	Input: None
	Output: None"""
		return self.nfstestsuites
		
	def setNfsTestResults(self):
		"""METHOD TIBoard.setNfsTestResults
	
	Input: None
	Output: None"""
		self.nfstestresults = self.settings.getKeyValue('nfs.testresults')
		return None
	
	def getNfsTestResults(self):
		"""METHOD TIBoard.getNfsTestResults
	
	Input: None
	Output: None"""
		return self.nfstestresults
	
	def sendOpenTCPSerialConnection(self):
		"""METHOD TIBoard.sendOpenTCPSerialConnection
	
	Input: None
	Output: None"""
		self.socket = TISocket.TISocket(self.settings.getKeyValue('tcp.serial.server.ip'),\
																		self.settings.getKeyValue('tcp.serial.server.port'))
		return None
		
	def closeOpenTCPSerialConnection(self):
		"""METHOD TIBoard.closeOpenTCPSerialConnection
	
	Input: None
	Output: None"""
		self.socket.close()
		return None

	
	def shellCommands(self):
		"""METHOD TIBoard.shellCommands
	
	Input: None
	Output: None"""	

		datetime = strftime("%m%d%H%M%Y", time.localtime())
		nfsTestSuites = self.settings.getKeyValue('nfs.testsuites')
		nfsTestResults = self.settings.getKeyValue('nfs.testresults')
		testResults = self.settings.getKeyValue('testResults')
		ipaddr = self.settings.getKeyValue('ipaddr')
		
		self.message.INFO('Already in shell... send required commands\n')
		self.message.INFO('')	
		self.socket.send('\r\rroot\r\rdate -s %s\r' % datetime, 1)
		self.socket.send('\r\recho %s > ipaddr\r' % ipaddr, 1)
		
		if self.testType != 'auto' and self.testType != 'manual':
			self.socket.send('\r\rifconfig eth0 up\r', 1)
			self.socket.send('\r\rifconfig eth0 %s\r' % ipaddr, 1)
			
		self.socket.send('\r\rmount -t nfs -o nolock,wsize=1024,rsize=1024 %s /automation/testsuites\r' % \
							(nfsTestSuites), 5)
		self.socket.send('\r\rmount -t nfs -o nolock,wsize=1024,rsize=1024 %s/%s /automation/testresults\r' % \
							(nfsTestResults, testResults), 1)
													
		username = self.settings.getKeyValue('username')
		self.message.INFO('')
		self.socket.send('/automation/testresults/test.list.sh | tee /automation/testresults/full.stdout.txt\r', 1)
		
		return None
