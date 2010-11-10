#!/usr/bin/python

import os, sys, commands, ConfigParser, re, time, shutil, urllib2, zipfile
from time import gmtime, strftime
import fileinput, string, random


def createTemporalFile(self):
	"""METHOD TITestListParser.createTemporalFile
Create a temporal file
Input: None
Output: None"""
	self.tempFile = tempfile.mktemp()
	self.logFile = open(self.tempFile, "w+b")
	os.chmod(self.tempFile , 0777)
	return None

def generateString(length):
	random.seed()
	d = [random.choice(string.letters) for x in xrange(length)]
	sstring = "".join(d)
	return sstring

def toZip(directory, zipFile, File=False):
  
	def walker( zip, directory, files, root=directory ):
		for file in files:
			file = os.path.join( directory, file )
			# yes, the +1 is hacky...
			archiveName = file[len(os.path.commonprefix( (root, file) ))+1:]
			print '---', archiveName
			zip.write( file, archiveName, zipfile.ZIP_DEFLATED )
			print file

	def single( zip, singlefile):
		#archiveName = file[len(os.path.commonprefix( ('./', file) ))+1:]
		#print '---', archiveName
		zip.write( singlefile, compress_type=zipfile.ZIP_DEFLATED )
		
	z = zipfile.ZipFile( zipFile, 'w', compression=zipfile.ZIP_DEFLATED )
	
	
	if File == True:
		single(z, directory)
	if File == False:
		os.path.walk( directory, walker, z )
    
	z.close()
	return zipFile

def toZip2( directory, zipFile):
    """Sample for storing directory to a ZipFile"""
    z = zipfile.ZipFile(
        zipFile, 'w', compression=zipfile.ZIP_DEFLATED
    )
    def walker( zip, directory, files, root=directory ):
        for file in files:
            file = os.path.join( directory, file )
            # yes, the +1 is hacky...
            archiveName = file[len(os.path.commonprefix( (root, file) ))+1:]
            zip.write( file, archiveName, zipfile.ZIP_DEFLATED )

    os.path.walk( directory, walker, z  )
    z.close()
    return zipFile
 
	
"""
	
"""  

def getPlatform(release, board):

	mainrelease = getMainRelease(release)
	platform='%s%s' % (mainrelease,board)
	
	return platform
	  

"""
	Determine the directory of the module
"""

def getModuleDirectory(fdReleaseDB, platform, module):
	if module == 'kernel':
		directory = getSingleValue(fdReleaseDB, platform, 'kernelPath')
	elif module == 'x-load':
		directory = getSingleValue(fdReleaseDB, platform, 'x-loadPath')
	elif module == 'u-boot':
		directory = getSingleValue(fdReleaseDB, platform, 'u-bootPath')
	return directory


"""
	Determine the name of the kernel to use
"""

def buildKernelName(uGet):
	
	release = uGet['release']
	board = uGet['board']
	driver = uGet['driver']
	kerneltype = uGet['uimage']
	
	if kerneltype == '':
		kernel = "uImage.%s.%s.%s.default" % (release, board, driver)
	else:
		kernel = kerneltype
		
	return kernel

"""
	Functions related to files
"""

def copyFile(src, dest):
	if os.path.exists(dest):
		os.remove(dest)
	try:
		shutil.copy(src, dest)
	except IOError:
		print 'Error trying to copy file'
	try:
		os.chmod(dest, 0777)
	except OSError:
		print 'Error trying to change permissions'

def setDirectory(directory):

	if os.path.exists(directory):
		shutil.rmtree(directory)

def doLocalCompilationSanity(uGet):
	
	directory_list = ['x-load_directory', 'u-boot_directory', 'kernel_directory']
	
	for each_element in directory_list:
		if each_element not in uGet:
			print '%s key not found in settings file %s' % (each_element, uGet['userfile'])
			sys.exit(1)

def readConfigurationFile(file):
	config = ConfigParser.ConfigParser()
	config.read(file)
	return config
	
def soutputFileToScreen(afile, lines=0):
	f = file(afile)
	lines_in_total = len(f.readlines())
	while True:
		line = f.readline()
		if len(line) == 0:
			break
		print line,
	f.close()

def outputFileToScreen(afile, lines=0):
	print '\n'
	counter = 0
	f = file(afile)
	all_lines = f.readlines()
	lines_in_total = len(all_lines)
	for line in all_lines:
		counter = counter + 1
		if lines == 'all':
			print '\t'+line.strip('\n')		
		else:
			if counter >= lines_in_total-lines:
				print '\t'+line.strip('\n')
	print '\n'				
	f.close()

def findStringInFile(file, tostring, errors=0):
	sys.stdout.write('\n')
	for line in fileinput.input(file):
		lineno = 0
		lineno = string.find(line, tostring)
		if lineno > 0:
			errors=1
			sys.stdout.write('\t%s' % line)
	sys.stdout.write('\n')
	sys.stdout.flush()

"""
	Functions related to Config Parser
"""

def getSingleValue(configid, component, tag):
	value = configid.get(component, tag)
	return value

def getColumnValue(uGet, option, column):
	value = uGet[option].split(':')
	return value[column]
	
"""
	Functions related to execution of commands
"""

def executeCommand(cmd):
	sys.stdout.write('\n\t%s' % cmd)
	sys.stdout.flush()
	status, output = commands.getstatusoutput(cmd)
	return status, output

def getMainRelease(release):
	if re.match('7x', release):
		mainrelease = '7x'
	elif re.search('8x14M', release):
		mainrelease = '8x14M'		
	elif re.match('8x', release):
		mainrelease = '8x'
	elif re.match('16x', release):
		mainrelease = '16x'	
	elif re.match('18x', release):
		mainrelease = '18x'
	elif re.search('12xNK', release):
		mainrelease = '12xNK'		
	elif re.search('12xNK', release):
		mainrelease = '12xNK'		
	elif re.match('12x', release):
		mainrelease = '12x'
	elif re.match('GITDISTx', release):
		mainrelease = 'GITDISTx'
	elif re.match('GITINTx', release):
		mainrelease = 'GITINTx'				
	
	return mainrelease


def requestWebServerCmd(uGet, cmd):

	if cmd == 'reset':
	
		webserverip = uGet['webserverip']
			
		mainWebServerCmd('http://%s/remote.cgi?formdata=remote_io_nen&pval=1' % webserverip)
		mainWebServerCmd('http://%s/remote.cgi?formdata=remote_io_nen&pval=0' % webserverip)
		mainWebServerCmd('http://%s/power.cgi?action=Power+Off' % webserverip)
		mainWebServerCmd('http://%s/power.cgi?action=Battery+Power' % webserverip)
		mainWebServerCmd('http://%s/power.cgi?action=Power+Off' % webserverip)		
		mainWebServerCmd('http://%s/power.cgi?action=DC+Power' % webserverip)
		#mainWebServerCmd('http://%s/power.cgi?action=S7' % webserverip)
		#mainWebServerCmd('http://%s/power.cgi?action=S5' % webserverip)
		mainWebServerCmd('http://%s/remote.cgi?formdata=remote_io_nen&pval=1' % webserverip)

def mainWebServerCmd(cmd):
	request = urllib2.Request(url=cmd)
	urllib2.urlopen(request)
	time.sleep(1)
	
"""
	Class connectTCP <> Send messages to TCP Serial Server
"""

class connectTCP:

	def __init__(self, sock = None):
		import socket
		if sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.sock = sock

	def connect(self, host, port):
		self.sock.connect((host, port))

	def sendCommands(self, level, array):
		for message in array:
			print '\t%s' % message
			messlen, received = self.sock.send(message), 0    
			if (re.search('^setenv', message)):
			        time.sleep(1)
			elif (re.search('^saveenv', message)):
				time.sleep(5)
			else:
				if level == 'boot':
					time.sleep(45)
				elif level == 'flash':
                                        time.sleep(5)
				else:
					time.sleep(2)

	def close(self):
		self.sock.close()


def verifyTCPconnection(ipaddr):

	print '\nChecking if IP %s is up' % ipaddr
	status = executeCommand('ping -c 2 %s' % ipaddr)
	if status <> 0:
		print '\n\nIP address is not available!!!\n'
	else:
		print '\n\nIP address %s is up!\n' % ipaddr

"""
def fexecuteCommand(cmd):	
	try:
		retcode = os.system(cmd)
		if retcode < 0:
			print >>sys.stderr, "Child was terminated by signal", -retcode
		else:
			print >>sys.stderr, "Child returned", retcode
	except OSError, e:
		print >>sys.stderr, "Execution failed:", e


def fexecuteCommand(cmd):

	status, output = commands.getstatusoutput(cmd)
	print "Output: ", output
	print "Status: ", status
	#pipe = os.popen(cmd)
	#r = pipe.read()
	#s = pipe.status()
	#print r, s
	
"""

"""
	Functions related to Drivers Configuration File
"""

def getPrefix(configid, driver):
	return configid.get(driver, "prefix")

def getDirName(configid, driver):
	return configid.get(driver, "dirname")

def getAllIx(configid, driver):
	list = []
	for eachfield in configid.options(driver):
		if eachfield != "prefix" and eachfield != "dirname":
			list.append(eachfield)
	list.sort()
	return list

def getAllKernelNames(configid):
	list = []

	list.sort()
	return list

"""
	Functions related to User Configuration File
"""

def getAllDrivers(configid):
	list = []
	for eachfield in configid.options('drivers'):
		if eachfield != 'times?':
			list.append(eachfield)
	list.sort()
	return list

def getDriverEnabled(configid, driver):
	if configid.get('drivers', driver) != 'y': 
		return 0
	else:
		return 1
		
def getAllDriversEnabled(configid):
	list = []
	for eachdriver in getAllDrivers(configid):
		if getDriverEnabled(configid, eachdriver) != 0:
			list.append(eachdriver)
	list.sort()
	return list


"""
	Other functions
"""

def getKernelType(configid, driver, option):
	line = configid.get(driver, option).split(';')
	return line[0]

def getBootArguments(configid, driver, option):
	line = configid.get(driver, option).split(';')
	return line[1]

def getTestType(configid, driver, option):
	line = configid.get(driver, option).split(';')
	return line[2]
	
def getParameters(configid, driver, option):
	line = configid.get(driver, option).split(';')
	return line[3]
	
def getScenarios(configid, driver, option):
	line = configid.get(driver, option).split(';')
	return line[4]				


"""

"""

def getPerformanceCases(configid):
	list = []
	for eachfield in configid.options('performance'):
		list.append(eachfield)
	list.sort()
	return list

def extractDrivers(templist):
	list = []
	list = templist.split(':')
	return list
	

def getScenariosList(configfile, driver, option):
	list = []
	item = configfile.get(driver, option).split(';')
	scenarios = item[4].split(',')
	prefix = getPrefix(configfile, driver)
	for eachscenario in scenarios:
		list.append(prefix+eachscenario)
	return list
	
def getTimestorun(configid, driver):
	return configid.get('drivers', 'times?')
	

	
