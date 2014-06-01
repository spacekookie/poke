#!/usr/bin/python

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
					or
		https://bitbucket.org/SpaceKookie/poke-ssh-utility

'''

import sys
import os.path
from subprocess import call
from optparse import OptionParser

''' This is an install helper to initiate the application on a new system '''
class Installer:

	def __init__(self, HOME, VERSION):
		self.HOME = HOME
		self.VERSION = VERSION

	def setup(self):
		print("Setting up poke on your machine...")
		if os.path.isdir(self.HOME + "/.poke") is False:
			call("mkdir ~/.poke", shell=True)
			call("chmod -R 766 ~/.poke", shell=True)

		# Because the config doesn't exist yet it needs to be created!
		configWriter = open(self.HOME + '/.poke/servers.cfg', 'wb+')
		header = ["Server config with poke v%s by Katharina Sabel (Updates may cause incompatibility)" % self.VERSION, "Email katharina.sabel@2rsoftworks.de suggestions and comments", "Visit support.2rsoftworks.de to report issues", "", "You can add your servers as sections below.", "Each section needs to have the Alias and URL field set but can have another field to determine", "if XTerm should be used for the SSH session.", "Note that the shorthands 'h', '?' and 'x' are reserved by the application.", "", "Name: Define a helpful name for your server", "ShortHand: short command-line argument", "LongHand: long command-line argument", "URL: server address", "User: server user (if needed)", "XDef: Default XTerm settings"]

		body = ["", "[SampleServer]", "Name: Jane's NAS", "ShortHand: j", "LongHand: jane", "URL: 111.222.333.444", "User: Jane", "XDef: False"]

		for item in header:
			if item == "":
				configWriter.write(item + "\n")
			else:
				configWriter.write("# " + item + "\n")
		for item in body:
			configWriter.write(item + "\n")
		configWriter.close()

		print "\nSuccessfully wrote 'server.cfg'. You should probably go to ~/.poke/ and set up your servers!\n"
		introParser = OptionParser()
		introParser.add_option("-?", action="store_false", help="Open 'Nano' to editor your server config")
		introParser.add_option("-x", action="store_false", default=False, help="Uses XTerm for the SSH session")
		print(introParser.format_help())
		sys.exit()

class KeyBase:

	def __init__(self):
		print "Managing Keys"

class UtilityFactory:

	def __init__(self, HOME, configReader):
		self.HOME = HOME
		self.configReader = configReader

	def GetSectionContents(self, section):
		dict1 = {}
		options = configReader.options(section)
		for option in options:
			try:
				dict1[option] = configReader.get(section, option)
				if dict1[option] == -1:
					DebugPrint("skip: %s" % option)
			except:
				print("exception on %s!" % option)
				dict1[option] = None
		return dict1

	def runNaNo(option, opt_str, value, parser):
		call("nano %s/.poke/servers.cfg" % self.HOME, shell=True)

	def getServerWithShorthand(shorty):
		info = {}
		options = configReader.sections()
		for s in options:
			serverShorty = ConfigSectionmMap(s)['shorthand']
			if serverShorty == shorty:
				info['url'] = ConfigSectionmMap(s)['url']
				info['user'] = ConfigSectionmMap(s)['user']
				if 'xdef' in ConfigSectionmMap(s):
					info['xdef'] = ConfigSectionmMap(s)['xdef']
		return info

	def validateServer(option, opt_str, value, parser):
		refactored = str(option)
		shortHand = refactored[1:2]

		# print shortHand
		global ServerURL
		ServerURL = getServerWithShorthand(shortHand)['url']

		global UserName
		UserName = getServerWithShorthand(shortHand)['user']
		if 'xdef' in ConfigSectionmMap(server):
			global UseXTerm
			UseXTerm = True
		else:
			UseXTerm = False

		global ServerSetupComplete
		if ServerURL is not None and UserName is not None: 
			ServerSetupComplete = True





