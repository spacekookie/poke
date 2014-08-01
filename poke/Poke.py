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

'''

from Controllers import CallbackController, PurgeController, UpgradeController
from optparse import OptionParser, SUPPRESS_HELP, OptionGroup
from IOHandle import Handle, ConfigHandle
from ConfigParser import ConfigParser
from datetime import datetime
from subprocess import call
from Strings import CCodes
from os import path, popen
from sys import exit, argv
from Intro import Setup
import textwrap

# This is the main application file and entry point for the Poke commandline tool.
class Poke():

	# Self variables
	home = path.expanduser("~") # Change this to move Poke-location (not recomended)
	version = "0.5.2"
	workingDirectory = ".poke" # Change this to rename working directory
	access = 1 # if 0 root is required to write and/or read ssh/ servers

	# rows, columns = popen('stty size', 'r').read().split()
	# cwidth = int(float(columns))

	def main(self):
		# If it went through the custom actions it will initiate itself!
		# Creates a starter object to init default values. If already set these will be read from config
		start = Setup(self.home, self.version, self.workingDirectory)
		start.make()

		global_config = ConfigHandle(self.home)
		cb = CallbackController(self.home, self.workingDirectory, global_config.read_configs())
		self.cc = CCodes()
		self.hadErrors = False

		# Checks if one of the two sub-modules was invoked.
		if len(argv) > 1:
			if argv[1] == "purge":
				p = PurgeController(self.home) #Ends session
			elif argv[1] == "upgrade":
				u = UpgradeController(False, self.version) #Ends session
			elif argv[1] == "upgrade-unstable":
				ret = raw_input(self.cc.WARNING + "==> Using unstable versions! Are you sure about that? [y/N]: " + self.cc.ENDC)
				if ret.lower() == "y":
					u = UpgradeController(True, self.version) #Ends session
				else:
					exit()
			
			# TODO: Get rid of this override. This should only be handled via the OptionsParser.
			# You shouldn't write your own little side-ways into certain parts of the application!
			elif argv[1] == "-?":
				cb.runEditor(None, None, None, None)

		# Future server to connect to!
		self.con = {}

		# Server config calls
		serverIO = Handle(self.home)
		self.serverCfg = ConfigParser()
		try:
			self.serverCfg.read(self.home + "/" + self.workingDirectory + "/servers.cfg")
		except Exception:
			print self.cc.FAIL + "MALFORMED KEY CONFIGURATION: MISSING KEY HEADER!" + self.cc.ENDC
			self.hadErrors = True
		self.servers = self.serverCfg.sections() # Contains server sections

		# Key config calls
		self.keyCfg = ConfigParser()
		try:
			self.keyCfg.read(self.home + "/" + self.workingDirectory + "/keys.cfg")
		except Exception:
			print self.cc.FAIL + "MALFORMED KEY CONFIGURATION: MISSING KEY HEADER!" + self.cc.ENDC
			self.hadErrors = True
		self.keys = self.keyCfg.sections()

		# Callbacks are handled automatically and need no further actions.
		parser = OptionParser(version=self.version)
		parser.remove_option("-h") # Remove default help from screen. TEMP WORKAROUND!

		# parser.add_option("upgrade", action="callback", help=SUPPRESS_HELP, callback=cb.helpMe)
		parser.add_option("-?", action="callback", help="Open preferred editor to edit your config files!", callback=cb.runEditor)

		administrative = OptionGroup(parser, "Overwrite Settings")
		administrative.add_option("-K", action="store", help="Overwrite stored key-setting for a server. Note: this is usually not very useful. Add the apropriate key to your keys.cfg file instead!", type="string", dest="SSH_KEY")
		administrative.add_option("-X", action="store_true", default=False, help="Overwrite XTerm settings for the ssh session", dest="xterm")
		parser.add_option_group(administrative)
		
		serverGroup = OptionGroup(parser, "Your servers")
		try:
			for server in self.servers:
				section = serverIO.getSectionMap(server, self.serverCfg)

				if 'name' in section:
					name = section['name']
				else:
					name = ""

				sHand = section['shorthand']

				if 'longhand' in section:
					lHand = section['longhand']
				else:
					lHand = ""
				url = section['url']
				user = section['user']

				if 'xdef' in section:
					if section['xdef'] == "True":
						xdef = "'True'"
					else:
						xdef = "'False'"
				else:
					xdef = "'False'"

				if 'key' in section:
					key = section['key']
				else:
					key = None

				serverID = name + (":[%s@%s]" % (user, url))
				if key is not None:
					helpText = "Connect to %s with key '%s'. XTerm is %s by default" % (serverID, key, xdef)
				else:
					helpText = "Connect to %s. XTerm is %s by default" % (serverID, xdef)
				serverGroup.add_option("-%s" % sHand, "--%s" % lHand, action="callback", help=helpText, callback=self.update)

				# action="store", type="string", dest="filename" 
		except Exception:
			print self.cc.FAIL + "MALFORMED SERVER CONFIGURATION!" + self.cc.ENDC
			self.hadErrors = True

		parser.add_option_group(serverGroup)
		(self.prefs, self.args) = parser.parse_args()

		# Displays the Poke help-text and added extra items for purge and upgrade. Will not display if {self.hadErrors = True}
		if len(argv) == 1:
			if not self.hadErrors:
				print(parser.format_help())
				print("Other commands:")
				print("  purge\t\t\tDeletes Poke from your system")
				print("  upgrade\t\tChecks if there are new stable releases of Poke")
				print("  upgrade-unstable\tAlso includes unstable releases in upgrade search")
				# wrapped = textwrap.wrap(upgradeMsg, width=self.cwidth)
				#for passage in wrapped:
				#print(upgradeMsg)
			else:
				print(self.cc.WARNING + "THE APPLICATION ENCOUNTERED FATAL ERRORS. FIX THEM. TERMINATING NOW!" + self.cc.ENDC)
			exit()
		else:
			# Checks if the configuration is empty
			if self.con != {}:
				self.action()
			else:
				print "You need to provide a server. Exiting..."
				exit()

	def action(self):
		if self.prefs.xterm:
			if self.con['xdef'] != self.prefs.xterm:
				print "Overwriting XTerm..."
			self.con['xdef'] = True

		if self.prefs.SSH_KEY:
			if self.con['key'] != self.prefs.SSH_KEY:
				print "Overwriting SSH Key..."
			self.con['key'] = self.prefs.SSH_KEY

		# Uses all the collected information to estabish SSH connection
		self.finalize()


	# Updates the global server stored in this class to connect to later!
	def update(self, option, opt_str, value, parser):
		t = str(option)
		handle = t[1:2]

		kCheck = Handle(self.home)
		keyList = {}
		try:
			for key in self.keys:
				section = kCheck.getSectionMap(key, self.keyCfg)
				keyList[section['id']] = section['path']
		except Exception:
			print(self.cc.WARNING + "MALFORMED KEY FILE!" + self.cc.ENDC)
			exit()

		sCheck = Handle(self.home)
		for server in self.servers:
			section = sCheck.getSectionMap(server, self.serverCfg)
			if section['shorthand'] == handle:
				self.con['name'] = section['name']
				self.con['url'] = section['url']
				self.con['user'] = section['user']
				if 'key' in section:
					tmp = section['key']
					self.con['key'] = sCheck.getGlobalURL(keyList[tmp])
				else:
					self.con['key'] = None

				if 'xdef' in section:
					if section['xdef'] == 'True':
						self.con['xdef'] = True
					else:
						self.con['xdef'] = False
				else:
					self.con['xdef'] = False

	def finalize(self):
		url = self.con['url']
		usr = self.con['user']
		if self.con['xdef']:
			x = " -X "
		else:
			x = " "
		
		if self.con['key'] is None:
			call("ssh " + usr + "@" + url + x, shell=True)
		else:
			call("ssh -i" + self.con['key'] + " " + usr + "@" + url + x, shell=True)

def run():
	startTime = datetime.now()
	var = datetime.now()-startTime
	try:
		Poke().main()
	except KeyboardInterrupt:
		print("\n\033[93mTriggered KeyboardInterrupt!\033[0m")
		exit()
	print("\033[92m==> SSH connection was open for %s \033[0m" % str(var))


# Starts the application
if __name__ == "__main__":
	startTime = datetime.now()
	var = datetime.now()-startTime
	try:
		Poke().main()
	except KeyboardInterrupt:
		print("\n\033[93mTriggered KeyboardInterrupt!\033[0m")
		exit()
	print("\033[92m==> SSH connection was open for %s \033[0m" % str(var))
