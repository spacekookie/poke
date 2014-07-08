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

class VersionController:
	pass
	
	def __init__(self, url, skeleton):
		self.url = url
		self.skeleton = skeleton

	def fetch(self):
		req = urllib2.Request(self.url)
		opener = urllib2.build_opener()
		f = opener.open(req)
		jdata = json.load(f)

class UpgradeController:
	pass
	
	# GitHub versioning URL
	url = 'https://api.github.com/repos/SpaceKookie/Poke/releases'

	# GitHub skeleton download URL
	skel = 'https://github.com/SpaceKookie/Poke/releases/download/'

	def __init__(self, unstable, version):
		self.forceLatest = False
		if unstable:
			print("Trying to determine if there are new unstable versions to patch to!")

		# Init the CCodes class (again)
		self.cc = CCodes()
		self.version = version

		# Getting root for the current process!
		if not geteuid()==0:
			print "==> Not running with root privileges. Trying to elevate via 'sudo'."
			call("sudo echo '%sSUCCESS!%s'" % (self.cc.OKGREEN, self.cc.ENDC), shell=True)

		if len(argv) == 3:
			if argv[1] == "upgrade":
				if argv[2] == "-f":
					self.forceLatest = True
			else:
				print(self.cc.WARNING + "Force upgrade only works for stable releases!" + self.cc.ENDC)

		print("Opening stream to www.github.com")
		# self.fetch()
		req = urllib2.Request(self.url)
		opener = urllib2.build_opener()
		f = opener.open(req)
		jdata = json.load(f)
		print(self.cc.OKGREEN + "==> Fetch complete. Analysing data..." + self.cc.ENDC)

		self.findCurrentVersion(jdata)
		# Goes through the data and copies the published-dates for analysis.
		dates = []
		for item in jdata:
			dates.append(item.get('created_at'))

		print(self.cc.OKGREEN + "==> Still analysing data..." + self.cc.ENDC)

		# Renders progress bar
		toolbar_width = 80
		stdout.write("[%s]" % (" " * toolbar_width))
		stdout.flush()
		stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['
		for i in xrange(toolbar_width):
		    time.sleep(0.005)
		    stdout.write(self.cc.OKBLUE + "#" + self.cc.ENDC)
		    stdout.flush()
		stdout.write("\n")

		# If only stable releases releases are considered.
		if unstable is False:
			for item in jdata:
				if item['prerelease'] is False:
					if self.isVersion(item['tag_name']):
						if self.compareVersionsBools(item['tag_name'], self.version):
							print(self.cc.WARNING + "==> Currently running version is outdated by an unstable package..." + self.cc.ENDC)
							self.info['version'] = item['tag_name']
							self.info['pack'] = "poke-" + item['tag_name'] + ".tar.bz2"
							self.info['url'] = self.skel + "/" + str(self.info['version']) + "/" + str(self.info['pack'])
						else:
							print(self.cc.WARNING + "==> No new stable releases to upgrade to!" + self.cc.ENDC)
							exit()
		else:
			for item in jdata:
				if item['prerelease'] is True:
					if self.isVersion(item['tag_name']):
						if self.compareVersionsBools(item['tag_name'], self.version):
							print(self.cc.WARNING + "==> Currently running version is outdated by an unstable package..." + self.cc.ENDC)
							self.info['version'] = item['tag_name']
							self.info['pack'] = "poke-" + item['tag_name'] + ".tar.bz2"
							self.info['url'] = self.skel + "/" + str(self.info['version']) + "/" + str(self.info['pack'])
						else:
							print(self.cc.WARNING + "==> No new unstable releases to upgrade to!" + self.cc.ENDC)
							exit()

		self.upgrade(self.info['url'], self.info['version'], False)
		exit()

	def fetch(self):
		req = urllib2.Request(self.url)
		opener = urllib2.build_opener()
		f = opener.open(req)
		jdata = json.load(f)

	# Compares two dates and returns the newer (larger) one
	def compareDates(self, a, b):
		if a > b:
			return a
		else:
			return b

	def isVersion(self, string):
		# Returns 'True' if string is a version string
		if len(string) == 5: 
			if string[1] == "." and string[3] == ".": return True
		return False

	def compareVersionsBools(self, a, b):
		def normalize(v):
			return [int(x) for x in sub(r'(\.+)*$','', v).split(".")]
		if normalize(a) > normalize(b):
			return True
		else:
			return False

	# Takes to x.y.z formatted version strings and returns the bigger one!
	def compareVersions(self, a, b):
		def normalize(v):
			return [int(x) for x in sub(r'(\.+)*$','', v).split(".")]
		if normalize(a) > normalize(b):
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

		self.info = {}
		self.info['version'] = self.version
		self.info['date'] = -1

	def upgrade(self, url, target, unstable):
		mst = "New version available. Would you like to upgrade to version %s now? [Y/n]: " % target
		blob = raw_input(mst)
		if blob.lower() == "n":
			print("==> Keeping old, outdated and smelly version...")
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
			return

		print(self.cc.OKGREEN + "==> Applying patch ..." + self.cc.ENDC)
		call("sudo chmod +x %stmp/dist/poke" % w, shell=True)
		call("sudo rm $(which poke)", shell=True)

		print("==> Moving binary to /usr/bin")
		call("sudo mv %stmp/dist/poke /usr/bin/poke" % w, shell=True)

		print("==> Cleaning up")
		call("rm -r %stmp/pyinstall %stmp/pyinstall.tar.gz  %stmp/dist/ %stmp/build/ %stmp/poke.spec %stmp/source/*.pyc" % (w, w, w, w, w, w), shell=True)
		call("sudo rm %s/poke.tar.bz2" % w, shell=True)

		if path.isdir('/usr/local/src/poke'):
			print("==> Moving new source files")
			call("sudo rm -r /usr/local/src/poke", shell=True)
			call("sudo mv %stmp /usr/local/src/poke" % w, shell=True)

		print(self.cc.OKGREEN + "==> Patcher shutting down. Run 'poke --version' to verify result!" + self.cc.ENDC)
		return