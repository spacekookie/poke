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


from datetime import datetime
from subprocess import call
from sys import exit

binary = False
source = False
config = False

print("This will remove poke from your /usr/bin directory.")
note = "Note you will have to execute this script with root privileges to remove poke correctly. Continue? [Y/n]: "

usrInput = raw_input(note)

if usrInput.lower() == "n":
	print("Canceling removal")
	exit()
elif usrInput.lower() == "y":
	pass
elif usrInput.lower() == "":
	pass
else:
	print "Invalid input. Canceling removal"
	exit()

call("sudo rm /usr/bin/poke", shell=True)
binary = True

print("")
askConfig = raw_input("Do you want to remove your config files from ~/.poke/? [Y/n]: ")

if askConfig.lower() == "n":
	print("Skipping config files")
	pass
else:
	call("rm -r ~/.poke/", shell=True)
	config = True

print ("")
askSource = raw_input("Do you want to remove the source-files from /usr/local/src/poke? (May include this script!) [Y/n]: ")

if askSource.lower() == "n":
	print("Skipping source files")
	pass
else:
	call("sudo rm -r /usr/local/src/poke", shell=True)
	source = True

if source and binary and config:
	print("Poke is now no longer installed on your system. I hope you're happy...")
elif binary and source:
	print("Poke binary and source are no longer on your machine. Config files are still present under ~/.poke")
elif binary and config:
	print("Poke binary and config are no longer on your machine. But you can always recompile the tool from source at /usr/local/src/poke")
else:
	print "Poke is still installed."