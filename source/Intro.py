#!usr/bin/python

from subprocess import call
from os import path
from sys import exit
import time
from Strings import Strings

class Setup:

	sDir = False
	sConf = False
	sServ = False
	sKeys = False

	# Writes a global config file into the .poke directory.
	def __init__(self, home, version, wDir):
		self.strBase = Strings(version)
		self.home = home
		self.version = version
		self.wDir = wDir
		self.setup = 0

	def createDirectory(self):
		print("Configuring application ...")
		call("mkdir %s/.poke" % self.home, shell=True)
		call("chmod -R 755 %s/.poke" % self.home, shell=True)
		self.sDir = True

	def createServerList(self):
		print("Writing server config")
		# TODO: READ WORKING DIRECTORY FROM CONFIG!
		servers = open(self.home + "/" + self.wDir + "/" + "servers.cfg", "wb+")
		for line in self.strBase.serverHead:
			if line == "":
				servers.write("\n")
			else:
				servers.write("# " + line + "\n")
		servers.write("\n")
		for line in self.strBase.serverBody:
			servers.write(line + "\n")

		servers.close()
		self.sServ = True

	def createKeyList(self):
		print "Writing keys config"

		keys = open(self.home + "/" + self.wDir + "/" + "keys.cfg", "wb+")
		for line in self.strBase.keyHead:
			keys.write("# " + line + "\n")
		keys.close()

		self.sKeys = True


	def createGlobalConfig(self):
		print("Writing global config")
		config = open(self.home + "/" + self.wDir + "/" + "global", 'wb+')

		for line in self.strBase.globalHead:
			config.write("# " + line + "\n")

		config.write("\n")
		config.write("Init on: " + time.strftime("%c") + "\n")
		config.write("$PATH:" + self.home + "\n")
		config.write("$DIR:" + ".poke" + "\n")
		config.write("$OS:" + "OSX" + "\n")
		config.write("$VER:" + self.version + "\n")

		config.close()
		self.sConf = True

	# Called on every run. Checks if the application has everything it needs to run.
	def make(self):
		# Means that the entire ~/.poke directory doesn't exist
		if path.isdir(self.home + "/.poke") is False:
			self.createDirectory()

		# Means that the global config is missing
		if path.isfile(self.home + "/.poke/global") is False:
			self.createGlobalConfig()

		# Means that the server config is missing
		if path.isfile(self.home + "/.poke/servers.cfg") is False:
			self.createServerList()

		# Means that the key config is missing
		if path.isfile(self.home + "/.poke/keys.cfg") is False:
			self.createKeyList()

		# Checks if something was missing before. Otherwise shuts up
		if self.sDir or self.sConf or self.sServ or self.sKeys:
			print("Part of the application config was missing. Type 'poke -?' to edit the configuration")
			# exit()

	def readConfig(self):
		config = open('', 'r')
