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
from subprocess import Popen, PIPE, call, check_call, CalledProcessError
from sys import exit
from os import environ, pathsep

startTime = datetime.now()
print("Welcome to the Poke build script Version 0.1")
print("This will compile poke and move the binary to your /usr/bin directory.")
note = "Note you will have to execute this script with root privileges to install poke correctly. Continue? [Y/n]: "

usrInput = raw_input(note)

if usrInput.lower() == "n":
	print("Canceling build")
	exit()
elif usrInput.lower() == "y":
	pass
elif usrInput.lower() == "":
	pass
else:
	print "Invalid input. Canceling build"
	exit()

print("Downloading compiler files...")
try:
	check_call(['wget'])
except CalledProcessError:
	print "Using wget"
	call("wget https://pypi.python.org/packages/source/P/PyInstaller/PyInstaller-2.1.tar.gz -O pyinstall.tar.gz", shell=True)
except OSError:
	print "Using curl"
	call("curl 'https://pypi.python.org/packages/source/P/PyInstaller/PyInstaller-2.1.tar.gz' -o 'pyinstall.tar.gz'", shell=True)

call("mkdir ./pyinstall && tar -vxzf pyinstall.tar.gz -C pyinstall --strip-components 1", shell=True)

print("Configuring application build file to system")

call("python pyinstall/utils/makespec.py -n poke -F source/*.py", shell=True)

print("\n")
print("Compiling application")
call("python pyinstall/pyinstaller.py poke.spec", shell=True)

print("\n")
print("Moving application to '/usr/bin'. THIS REQUIRES ROOT PRIVILEGES!")

call("chmod +x dist/poke", shell=True)
call("sudo mv dist/poke /usr/bin/poke", shell=True)

print("Cleaning up after myself...")
call("rm -r pyinstall pyinstall.tar.gz  dist/ build/ poke.spec source/*.pyc", shell=True)

print("\n")
check = raw_input("Do you want me to link the '/usr/bin' to your path (if not already)? [Y/n]: ")

if check.lower() == "y" or check.lower() == "":
	path = environ['PATH'].split(pathsep)
	if not'/usr/bin' in path:
		call("export PATH='$PATH:/usr/bin'", shell=True)
else:
	print "Not linking directory..."

print("\n")
print "Would you like to move the source files of Poke to a more convenient location? (/usr/local/src)"
source = raw_input("You will be able to re-compile Poke from there or remove it if you so desire without having to download any additional files. [Y/n]: ")

if source.lower() == "n":
	pass
else:
	call("sudo mkdir -p /usr/local/src", shell=True)
	call("cd .. && sudo cp -r Poke /usr/local/src/poke", shell=True)

time = (datetime.now()-startTime)
print("\n")
print("The script is now finished. I took %s to run. Type 'poke' to configure the application" % time)
exit()