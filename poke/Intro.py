#!usr/bin/python

'''

Copyright (c) 2014 Katharina Sabel <katharina.sabel@2rsoftworks.de>
Copyright (c) 2014 Random Robot Softworks
www.katharinasabel.de | www.2rsoftworks.de

Licensed under the Apache License, Version 2.0 (the "License");		
you may not use this file except in compliance with the License.		
You may obtain a copy of the License at	

		http://www.apache.org/licenses/LICENSE-2.0						
									
Unless required by applicable law or agreed to in writing, software	
distributed under the License is distributed on an "AS IS" BASIS,		
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Found a bug? Report it in the repository issue tracker:

		https://github.com/SpaceKookie/Poke

'''

from subprocess import call
from os import path
from sys import exit
import time
import platform
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
		for line in self.strBase.keyBody:
			keys.write(line + "\n")
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
		config.write("$OS:" + platform.system() + " " + platform.release() + "\n")
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
			exit()

	def readConfig(self):
		config = open('', 'r')
