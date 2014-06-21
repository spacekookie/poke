#!/usr/bin/python

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
        call("wget 'https://pypi.python.org/packages/source/P/PyInstaller/PyInstaller-2.1.tar.gz' -o 'pyinstall.tar.gz'", shell=True)
except OSError:
        call("curl 'https://pypi.python.org/packages/source/P/PyInstaller/PyInstaller-2.1.tar.gz' -o 'pyinstall.tar.gz'", shell=True)

call("mkdir ./pyinstall && tar -vxzf pyinstall.tar.gz -C pyinstall --strip-components 1", shell=True)

print("Configuring application build file to system")

call("python pyinstall/utils/makespec.py -n poke -F source/*.py", shell=True)

print("Compiling application")

call("python pyinstall/pyinstaller.py poke.spec", shell=True)

print("Moving application to '/usr/bin'. THIS REQUIRES ROOT PRIVILEGES!")

call("chmod +x dist/poke", shell=True)
call("sudo mv dist/poke /usr/bin/poke", shell=True)

print("Cleaning up after myself...")

call("rm -r pyinstall pyinstall.tar.gz  dist/ build/ poke.spec", shell=True)

check = raw_input("Do you want me to link the '/usr/bin' to your path (if not already)? [Y/n]: ")

if check.lower() == "y" or check.lower() == "":
	path = environ['PATH'].split(pathsep)
		if not'/usr/bin' in path:
			call("export PATH='$PATH:/usr/bin'", shell=True)
		else:
			print "/usr/bin/ is alrady linked in path. Omitting export..."	
else:
	print "Not linking directory..."

time = (datetime.now()-startTime)
print("The script is now finished. I took %s to run. Type 'poke' to configure the application" % time)
exit()