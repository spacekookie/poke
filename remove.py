#!/usr/bin/python

from datetime import datetime
from subprocess import call
from sys import exit

print("This will remove poke from your /usr/sbin directory.")
print("This will *not* remove your configuration files from ~/.poke")
note = "Note you will have to execute this script with root privileges to install poke correctly. Continue? [Y/n]: "

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

call("sudo rm /usr/sbin/poke", shell=True)

print("Removal complete.")