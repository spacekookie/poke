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
from os import geteuid, path
from sys import exit
from subprocess import call, Popen, PIPE
from Strings import Strings, CCodes


class CallbackController:

	def __init__(self, home, wdir):
		self.home = home
		self.wdir = wdir

	def runVi(self, option, opt_str, value, parser):
		call("vi " + self.home + "/" + self.wdir, shell=True)
		exit()

	def helpMe(self, option, opt_str, value, parser):
		print("Something helpful here")
		exit()

class PurgeController:

	def __init__(self, home):
		self.binary = False
		self.source = False
		self.config = False
		self.cc = CCodes()
		self.strings = Strings(None)
		self.home = home

		print(self.cc.WARNING + "==> YOU ARE ABOUT TO PURGE POKE FROM YOUR SYSTEM !!!\n" + self.cc.ENDC)
		note = "I will need root privileges to remove Poke correctly. Continue? [Y/n]: "
		usrInput = raw_input(note)

		if usrInput.lower() == "n":
			print(self.cc.OKGREEN + "==> PURGE CANCELED" + self.cc.ENDC)
			exit()
		elif usrInput.lower() == "y":
			pass
		elif usrInput.lower() == "":
			pass
		else:
			print(self.cc.OKGREEN + "Invalid input. PURGE CANCELED" + self.cc.ENDC)
			exit()

		if not geteuid()==0:
			print "==> Not running with root privileges. Trying to elevate via 'sudo'."
			call("sudo echo '\033[92mSUCCESS!\033[0m'", shell=True)

		askBin = raw_input("Remove binary from '/usr/bin'? [Y/n]: ").lower()
		if askBin.lower() == "y" or askBin.lower() == "":
			self.purgeBinary()
		
		askSource = raw_input("Remove source files from '/usr/local/src'? [Y/n]: ").lower()
		if askSource.lower() == "y" or askSource.lower() == "":
			self.purgeSource()
		
		askConf = raw_input("Remove configuration files from '~/.poke'? [Y/n]: ").lower()
		if askConf.lower() == "y" or askConf.lower() == "":
			self.purgeConfigs()

		if self.source and self.binary and self.config:
			print(self.cc.HEADER + "==> Poke is now no longer installed on your system. I hope you're happy... :(" + self.cc.ENDC)
		elif self.binary and self.source:
			print(self.cc.HEADER + "==> Poke binary and source are no longer on your machine. Config files are still present under ~/.poke" + self.cc.ENDC)
		elif self.binary and self.config:
			print(self.cc.HEADER + "==> Poke binary and config are no longer on your machine. But you can always recompile the tool from source at /usr/local/src/poke" + self.cc.ENDC)
		else:
			print "==> Poke is still installed."
		print "Either way: Terminating!"
		exit()

	def purgeBinary(self):
		pipe = Popen(['which', 'poke'], stdout=PIPE, stdin=PIPE)
		text = pipe.communicate()[0]
		if not text:
			print("Poke binary couldn't be found on this system!")
		else:
			call("sudo rm %s" % text, shell=True)
			print(self.cc.OKGREEN + "SUCCESS!" + self.cc.ENDC)
			self.binary = True

	def purgeSource(self):
		if path.isdir("/usr/local/src/poke") is True:
			call("sudo rm -r /usr/local/src/poke", shell=True)
			print(self.cc.OKGREEN + "SUCCESS!" + self.cc.ENDC)
			self.source = True
		else:
			print(self.cc.WARNING + "Source files weren't found at expected location. Do they even exist?" + self.cc.ENDC)

	def purgeConfigs(self):
		if path.isdir(self.home + "/.poke"):
			call("rm -r ~/.poke/", shell=True)
			print(self.cc.OKGREEN + "SUCCESS!" + self.cc.ENDC)
			self.config = True
		else:
			print(self.cc.WARNING + "I couldn't find any configs!" + self.cc.ENDC)

class UpgradeController:

	def __init__(self):
		print "This feature is currently not (yet) implemented!"
		exit()