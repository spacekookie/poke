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
from subprocess import Popen, PIPE, call, check_call, CalledProcessError
from os import environ, pathsep, path, geteuid, popen
from textwrap import wrap
from datetime import datetime
from sys import exit, argv

try:
	rows, columns = popen('stty size', 'r').read().split()
	width = int(float(columns))
	startTime = datetime.now()

	if len(argv) == 2:
		if argv[1] == "install":
			if path.isfile('dist/poke'):
				if not geteuid()==0:
					print "\033[93mNot running with root privileges. Trying to elevate via 'sudo'.\033[0m"
					try:
						call("sudo echo '\033[92mSUCCESS!\033[0m'", shell=True)
					except KeyboardInterrupt:
						print("Canceling install!")
						exit()

				binary = False
				source = False

				print("\033[95m==> Installing application to /usr/local/bin/\033[0m")
				call("sudo chmod +x dist/poke", shell=True)
				try:
					call("sudo mv dist/poke /usr/local/bin/poke", shell=True)
					print("Successfully moved binary to /usr/local/bin!")
					binary = True
				except Exception:
					print("Error while moving binary!")

				cpath = raw_input("\033[95m==> Link /usr/local/bin to $PATH? [Y/n]: \033[0m")
				if cpath.lower() == "y" or cpath.lower() == "":
					path = environ['PATH'].split(pathsep)
					if not'/usr/local/bin' in path:
						call("export PATH='$PATH:/usr/local/bin'", shell=True)
						print("Successfully linked $PATH!")
					else:
						print("/usr/local/bin already in $PATH!")
				else:
					print("Not linking directory to $PATH!")

				csource = raw_input("\033[95m==> Move source files to '/usr/local/src'?\033[0m\nYou will be able to re-compile Poke from there\nor remove it if you so desire without having to download any additional files [Y/n]: ")
				if csource.lower() == "y" or csource.lower() == "":
					call("sudo mkdir -p /usr/local/src", shell=True)
					call("cd .. && sudo cp -r Poke /usr/local/src/poke", shell=True)
					source = True

				print("I'm done doin stuff now. Cleaning up after myself...")
				call("rm -r pyinstall pyinstall.tar.gz  dist/ build/ poke.spec source/*.pyc", shell=True)
				if binary:
					final = "\033[92m==> You now have a binary in /usr/local/bin"
				else:
					final = "\033[91m==> Copying the binary to /usr/local/bin failed!"
				if source:
					final = final + " and your source files are at /usr/local/src/poke!\033[92m"
				print(final)
				print("\n==> Type 'poke' to configure the application\n")
				print("\033[92mMy job is done. Good bye! <3\033[0m")
				exit()

			else:
				print("\033[95mYou need to run './make' first!\033[0m")
				exit()

	# This will run ./make NOT ./make install!
	print("\033[95m==> Welcome to Poke <==\033[0m")
	usrInput = raw_input("I will \033[95mdownload additional\033[0m compiler files and compile this application for you. Continue? [Y/n]: ")
	if usrInput.lower() == "n":
		print("\033[91m==> Canceling build\033[0m")
		exit()

	print("\033[92m==> Downloading compiler files.\033[0m")
	try:
		check_call(['wget'])
	except CalledProcessError:
		print("\033[92m==> USING WGET.\033[0m")
		call("wget https://pypi.python.org/packages/source/P/PyInstaller/PyInstaller-2.1.tar.gz -O pyinstall.tar.gz", shell=True)
	except OSError:
		print("\033[92m==> USING CURL.\033[0m")
		call("curl 'https://pypi.python.org/packages/source/P/PyInstaller/PyInstaller-2.1.tar.gz' -o 'pyinstall.tar.gz'", shell=True)

	print("\033[92m==> Extracing compiler files!\033[0m")
	call("mkdir ./pyinstall && tar -vxzf pyinstall.tar.gz -C pyinstall --strip-components 1", shell=True)

	print("\033[92m==> Configuring application build file to system\033[0m")
	call("python pyinstall/utils/makespec.py -n poke -F poke/*.py", shell=True)

	print("\n")
	print("\033[92m==> Compiling application\033[0m")
	call("python pyinstall/pyinstaller.py poke.spec", shell=True)

	if path.isfile('dist/poke'):
		print("\033[92m==> Compile complete! Now run './make install' (needs root) to install poke to your system!\033[0m")
	else:
		er = "==> Something went wrong during compiling. Would you please consider heading over to www.github.com/SpaceKookie/Poke and creating a new issue with the stack trace and the version you were trying to compile? Thank you :) <3"
		errorList = wrap(er, width=width)
		for element in errorList:
			print("\033[91m" + element + "\033[0m")

	print("\033[95mTerminating...\033[0m")
	exit()
except KeyboardInterrupt:
	print("\n\n\033[91mKEYBOARDINTERRUPT FIRED!\033[0m")
	exit()