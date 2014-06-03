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
					or
		https://bitbucket.org/SpaceKookie/poke-ssh-utility

'''

from optparse import OptionParser
from subprocess import call
import ConfigParser
import os.path
import sys
import time
from util import Installer

#Home variable for python paths
HOME = os.path.expanduser("~")
VERSION = "0.2.1"

# Creating setup object just in case.
setup = Installer(HOME, VERSION)
serverSetup = False
keySetup = False

# Checks if the application header file exists. Header file will contain logs and changes
if os.path.isfile(HOME + "/.poke/.a") is False:
	HEADER = open(HOME + '/.poke/.a', 'wb+')
	HEADER.write("Init Application on " + time.strftime("%c"))
	HEADER.close()

if os.path.isfile(HOME + "/.poke/servers.cfg") is False:
	serverSetup = setup.servers()

if os.path.isfile(HOME + "/.poke/keys.cfg") is False:
	keySetup = setup.keys()

# Exists the application without setting up server info. Only
if(serverSetup and keySetup):
	introParser = OptionParser()
	introParser.add_option("-?", action="store_false", help="Open 'Vi' to editor your config files!", callback=runVi)
	introParser.add_option("-x", action="store_false", default=False, help="Uses XTerm for the SSH session")
	print(introParser.format_help())
	sys.exit()

# If system is already set up the script will skip to HERE!

configReader = ConfigParser.ConfigParser()
configReader.read(HOME + "/.poke/servers.cfg")

def ConfigSectionmMap(section):
	dict1 = {}
	options = configReader.options(section)
	for option in options:
		try:
			dict1[option] = configReader.get(section, option)
			if dict1[option] == -1:
				DebugPrint("skip: %s" % option)
		except:
			print("exception on %s!" % option)
			dict1[option] = None
	return dict1

def runVi(option, opt_str, value, parser):
	call("vi %s/.poke/" % HOME, shell=True)

# Options Paser
parser = OptionParser(version="%s" % VERSION)
parser.add_option("-?", action="callback", help="Open 'Vi' to editor your config files!", callback=runVi)
parser.add_option("-x", action="store_true", help="Overwrite XTerm settings for the ssh session", dest="xterm")

servers = configReader.sections()

# Global SSH connection variables:
ServerURL = None
UserName = None
UseXTerm = False
ServerSetupComplete = None

def getServerWithShorthand(shorty):
	info = {}
	options = configReader.sections()
	for s in options:
		serverShorty = ConfigSectionmMap(s)['shorthand']
		if serverShorty == shorty:
			info['url'] = ConfigSectionmMap(s)['url']
			info['user'] = ConfigSectionmMap(s)['user']
			if 'xdef' in ConfigSectionmMap(s):
				info['xdef'] = ConfigSectionmMap(s)['xdef']
	return info

def validateServer(option, opt_str, value, parser):
	refactored = str(option)
	shortHand = refactored[1:2]

	# print shortHand
	global ServerURL
	ServerURL = getServerWithShorthand(shortHand)['url']

	global UserName
	UserName = getServerWithShorthand(shortHand)['user']
	if 'xdef' in ConfigSectionmMap(server):
		global UseXTerm
		UseXTerm = True
	else:
		UseXTerm = False

	global ServerSetupComplete
	if ServerURL is not None and UserName is not None: 
		ServerSetupComplete = True

#Loop through server config and display an item in the help-screen
for server in servers:
	name = ConfigSectionmMap(server)['name']
	sHand = ConfigSectionmMap(server)['shorthand']
	lHand = ConfigSectionmMap(server)['longhand']
	url = ConfigSectionmMap(server)['url']
	user = ConfigSectionmMap(server)['user']
	if 'xdef' in ConfigSectionmMap(server):
		xdef = "'%s'" % ConfigSectionmMap(server)['xdef']
	else:
		xdef = "'False'"
	serverID = name + (":[%s@%s]" % (user, url))
	parser.add_option("-%s" % sHand, "--%s" % lHand, action="callback", help="Connect to %s. XTerm is %s by default" % (serverID, xdef), callback=validateServer)

(prefs, args) = parser.parse_args()

# Display the help-screen if nothing else was selected
if len(sys.argv) == 1:
	print(parser.format_help())
	sys.exit()

def getXTermSetting():
	if UseXTerm:
		return "-X"
	else:
		return ""

if ServerSetupComplete:
	print "Connecting to server %s@%s" % (UserName, ServerURL)
	if prefs.xterm:
		print "Overwriting stored XTerm Settings"
		UseXTerm = True
	call("ssh %s@%s %s" % (UserName, ServerURL, getXTermSetting()), shell=True)