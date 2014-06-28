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
from Strings import Strings, CCodes
from sys import exit,stdout
from textwrap import wrap
import urllib2
import json
import time


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
	url = 'https://api.github.com/repos/SpaceKookie/Poke/releases'
	skel = 'https://github.com/SpaceKookie/Poke/releases/download/'

	def __init__(self, unstable, version):
		if unstable:
			print("This feature is currently still not implemented. Please only upgrade to stable versions!")
			exit()

		# Init the CCodes class (again)
		self.cc = CCodes()
		self.version = version

		# Getting root for the current process!
		if not geteuid()==0:
			print "==> Not running with root privileges. Trying to elevate via 'sudo'."
			call("sudo echo '\033[92mSUCCESS!\033[0m'", shell=True)

		print("Opening stream to www.github.com")
		req = urllib2.Request(self.url)
		opener = urllib2.build_opener()
		f = opener.open(req)
		jdata = json.load(f)
		print(self.cc.OKGREEN + "==> Fetch complete. Analysing data..." + self.cc.ENDC)

		self.findCurrentVersion(jdata)
		# Goes through the data and copies the published-dates for analysis.
		dates = []
		for item in jdata:
			dates.append(item.get('published_at'))

		print(self.cc.OKGREEN + "==> Still analysing data..." + self.cc.ENDC)

		toolbar_width = 80
		stdout.write("[%s]" % (" " * toolbar_width))
		stdout.flush()
		stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

		for i in xrange(toolbar_width):
		    time.sleep(0.005)
		    stdout.write(self.cc.OKBLUE + "#" + self.cc.ENDC)
		    stdout.flush()
		stdout.write("\n")

		if dates[0] <= self.info['date']:
			print(self.cc.OKGREEN + "==> You're already running the latest version of Poke." + self.cc.ENDC)
			print("Terminating...")
			exit()
		else:
			if not unstable:
				for item in jdata:
					if item['tag_name'] == 'stable':
						assets = item['assets']
						for asset in assets:
							name = asset['name']
							if name.endswith('tar.bz2'):
								url = self.skel + "stable/" + name
								self.info['url'] = url

		self.upgrade(self.info['url'], name[5:10], False)

	# Compares two dates and returns the newer (larger) one
	def compareDates(self, a, b):
		if a > b:
			return a
		else:
			return b

	#poke-0.4.5.tar.bz2 5-10
	# Magic that determines the date of the version currently running!
	def findCurrentVersion(self, jdata):
		targets = []
		for item in jdata:
			assets = item['assets']
			versions = {}

			for asset in assets:
				if asset['name'].endswith('.tar.bz2'):
					versions['packs'] = asset['name']
					versions['version'] = asset['name'][5:10]
					versions['date'] = asset['created_at']
			targets.append(versions)
		
		for target in targets:
			if target['version'] == self.version:
				print (self.cc.HEADER +"==> You are currently running Poke version " + self.version + " which was released on " + target['date']+ self.cc.ENDC)
				self.info = {}
				self.info['version'] = target['version']
				self.info['date'] = target['date']
				self.info['packs'] = target['packs']
				return

	def getLatestUnstable(self, versions):
		pass

	def upgrade(self, url, target, unstable):
		if unstable:
			print("Downloading latest unstable version. You have been warned.")

		mst = "New version available. Would you like to upgrade to version %s now? [Y/n]: " % target
		blob = raw_input(mst)
		if blob.lower() == "n":
			return

		w = "~/.poke/"
		rows, columns = popen('stty size', 'r').read().split()
		home = path.expanduser("~")
		width = int(float(columns))

		call("sudo cd ~/.poke", shell=True)
		print("Opening stream to www.github.com")
		try:
			check_call(['wget'])
		except CalledProcessError:
			print(self.cc.HEADER + "==> USING WGET." + self.cc.ENDC)
			call("wget %s -O ~/.poke/poke.tar.bz2" % url, shell=True)
		except OSError:
			print(self.cc.HEADER + "==> USING CURL." + self.cc.ENDC)
			call("curl '%s' -o '~/.poke/poke.tar.bz2'" % url, shell=True)

		# Extracting the files to a neutral folder with no version string on it
		call("mkdir %stmp && tar -xjvf %spoke.tar.bz2 -C %stmp/ --strip-components 1" % (w, w, w), shell=True)

		print(self.cc.OKGREEN + "==> Installing patch %s" % target + self.cc.ENDC)

		print("==> Welcome to the friendly patching system")
		print(self.cc.OKGREEN + "==> Configuring patcher..." + self.cc.ENDC)
		call("python %stmp/pyinstall/utils/makespec.py -n poke -F %stmp/source/*.py" % (w, w), shell=True)

		print("\n")
		print(self.cc.OKGREEN + "==> Downloading compiler files" + self.cc.ENDC)
		try:
			check_call(['wget'])
		except CalledProcessError:
			print(self.cc.OKGREEN + "==> USING WGET" + self.cc.ENDC)
			call("wget https://pypi.python.org/packages/source/P/PyInstaller/PyInstaller-2.1.tar.gz -O %stmp/pyinstall.tar.gz" % w, shell=True)
		except OSError:
			print(self.cc.OKGREEN + "==> USING CURL" + self.cc.ENDC)
			call("curl 'https://pypi.python.org/packages/source/P/PyInstaller/PyInstaller-2.1.tar.gz' -o '%stmp/pyinstall.tar.gz'" % w, shell=True)

		print(self.cc.OKGREEN + "==> Unpacking compiler ..." + self.cc.ENDC)
		call("mkdir %stmp/pyinstall && tar -vxzf %stmp/pyinstall.tar.gz -C %stmp/pyinstall --strip-components 1" % (w, w, w), shell=True)
		
		print(self.cc.OKGREEN + "==> Configuring compiler ..." + self.cc.ENDC)
		call("python %stmp/pyinstall/utils/makespec.py -n %stmp/poke -F %stmp/source/*.py" % (w, w, w), shell=True)
		
		print(self.cc.OKGREEN + "==> Compiling patch ..." + self.cc.ENDC)
		call("cd %stmp/ && python pyinstall/pyinstaller.py poke.spec" % w, shell=True)


		if path.isfile(home + '/.poke/tmp/dist/poke'):
					print(self.cc.OKGREEN + "==> Patch %s compiled successfully!\n" % target + self.cc.ENDC)
		else:
			er = "==> Something went wrong while patching. Would you please consider heading over to www.github.com/SpaceKookie/Poke and creating a new issue with the stack trace and the version you were trying to compile? Thank you :) <3"
			errorList = wrap(er, width=width)
			for element in errorList:
				print(self.cc.FAIL + element + self.cc.ENDC)
			exit()

		print(self.cc.OKGREEN + "==> Applying patch ..." + self.cc.ENDC)
		call("sudo chmod +x %stmp/dist/poke" % w, shell=True)
		call("sudo rm $(which poke)", shell=True)

		print("==> Moving binary to /usr/bin")
		call("sudo mv %stmp/dist/poke /usr/bin/poke" % w, shell=True)

		print("==> Cleaning up")
		call("rm -r %stmp/pyinstall %stmp/pyinstall.tar.gz  %stmp/dist/ %stmp/build/ %stmp/poke.spec %stmp/source/*.pyc" % (w, w, w, w, w, w), shell=True)

		if path.isdir('/usr/local/src/poke'):
			print("==> Moving new source files")
			call("sudo rm -r /usr/local/src/poke", shell=True)
			call("sudo mv %stmp /usr/local/src/poke" % w, shell=True)

		print(self.cc.OKGREEN + "==> Patcher shutting down. Run 'poke --version' to verify result!" + self.cc.ENDC)
		exit()


















