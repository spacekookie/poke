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

from sys import exit
from subprocess import call
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

	def __init__(self):
		print "Hello???"
		self.binary = False
		self.source = False
		self.config = False
		self.cc = CCodes()

		print("!!! YOU ARE ABOUT TO PURGE POKE FROM YOUR SYSTEM !!!\n")
		note = "Note you will have to execute this script with root privileges to remove Poke correctly. Continue? [Y/n]: "
		usrInput = raw_input(note)

		if usrInput.lower() == "n":
			print("PURGE CANCELED")
			exit()
		elif usrInput.lower() == "y":
			pass
		elif usrInput.lower() == "":
			pass
		else:
			print "Invalid input. PURGE CANCELED"
			exit()

		purgeBinary()

		purgeSource()

		purgeConfigs()



	def purgeBinary(self):
		pass

	def purgeSource(self):
		if path.isdir(self.home + "/usr/local/src/poke") is True:
			call("rm -r /usr/local/src/poke", shell=True)
		else:
			msg = cc.WARNING + "!!!EXPERIMENTAL!!! source couldn't be found at '/usr/local/src/poke'. Did you install it somewhere else? Do you want me to to search for it? [y/N]: " + cc.ENDC
			feedback = raw_input(msg) # Move message to Strings class

			if feedback.lower() == "y":
				print "This may take a while!"
				call("find / | grep 'poke' >> .temp", shell=True)
			else:
				print "Not removing source from system."

	def purgeConfigs(self):
		call("rm -r ~/.poke/", shell=True)
		self.config = True

