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

from Strings import CCodes, PurgeDiag

''' Class to get rid of Poke installation on a system and all it's files '''
class PurgeController:

	def __init__(self, home):
		self.binary = False
		self.source = False
		self.config = False
		self.cc = CCodes()
		self.pd = PurgeDiag()
		self.home = home

		print(self.cc.WARNING + self.pd.init_head + self.cc.ENDC)
		usr_response = raw_input(self.pd.init_check)

		if usr_response.lower() == "n":
			print(self.cc.OKGREEN + self.pd.init_canceled + self.cc.ENDC)
			exit()
		elif usr_response.lower() == "y":
			pass
		elif usr_response.lower() == "":
			pass
		else:
			print(self.cc.OKGREEN + "Invalid input. PURGE CANCELED" + self.cc.ENDC)
			exit()

		if not geteuid()==0:
			print self.cc.WARNING + "==> Not running with root privileges. Trying to elevate via 'sudo'." + self.cc.ENDC
			call("sudo echo '\033[92mSUCCESS!\033[0m'", shell=True)

		askBin = raw_input("Remove binary from '/usr/local/bin'? [Y/n]: ").lower()
		if askBin.lower() == "y" or askBin.lower() == "":
			self.purgeBinary()
		else:
			print(self.cc.WARNING + "SKIPPED" + self.cc.ENDC)
		
		askSource = raw_input("Remove source files from '/usr/local/src'? [Y/n]: ").lower()
		if askSource.lower() == "y" or askSource.lower() == "":
			self.purgeSource()
		else:
			print(self.cc.WARNING + "SKIPPED" + self.cc.ENDC)
		
		askConf = raw_input("Remove configuration files from '~/.poke'? [y/N]: ").lower()
		if askConf.lower() == "y":
			self.purgeConfigs()
		else:
			print(self.cc.WARNING + "SKIPPED" + self.cc.ENDC)

		if self.source and self.binary and self.config:
			print(self.cc.HEADER + "==> Poke is now no longer installed on your system. I hope you're happy... :(" + self.cc.ENDC)
		elif self.binary and self.source:
			print(self.cc.HEADER + "==> Poke binary and source are no longer on your machine. Config files are still present under ~/.poke" + self.cc.ENDC)
		elif self.binary and self.config:
			print(self.cc.HEADER + "==> Poke binary and config are no longer on your machine. But you can always recompile the tool from source at /usr/local/src/poke" + self.cc.ENDC)
		else:
			print(self.cc.OKGREEN + "==> Poke is still installed." + self.cc.ENDC)
		exit()

	def purgeBinary(self):
		pipe = Popen(['which', 'poke'], stdout=PIPE, stdin=PIPE)
		text = pipe.communicate()[0]
		self.binary = True
		if not text:
			print(self.cc.WARNING + "Poke binary couldn't be found on this system!" + self.cc.ENDC)
		else:
			call("sudo rm %s" % text, shell=True)
			print(self.cc.OKGREEN + "SUCCESS!" + self.cc.ENDC)

	def purgeSource(self):
		self.source = True
		if path.isdir("/usr/local/src/poke") is True:
			call("sudo rm -r /usr/local/src/poke", shell=True)
			print(self.cc.OKGREEN + "SUCCESS!" + self.cc.ENDC)
		else:
			print(self.cc.WARNING + "Source files weren't found at expected location. Do they even exist?" + self.cc.ENDC)

	def purgeConfigs(self):
		self.config = True
		if path.isdir(self.home + "/.poke"):
			call("rm -r ~/.poke/", shell=True)
			print(self.cc.OKGREEN + "SUCCESS!" + self.cc.ENDC)
		else:
			print(self.cc.WARNING + "I couldn't find any configs!" + self.cc.ENDC)
