#!/usr/bin/python

#############################################################################
# Copyright (c) 2014 Katharina Sabel <katharina.sabel@2rsoftworks.de>		#
# www.katharinasabel.de | www.2rsoftworks.de								#
# 																			#
# Licensed under the Apache License, Version 2.0 (the "License");			#
# you may not use this file except in compliance with the License.			#
# You may obtain a copy of the License at									#
# 																			#
#        http://www.apache.org/licenses/LICENSE-2.0							#
# 																			#
# 																			#
# Unless required by applicable law or agreed to in writing, software		#
# distributed under the License is distributed on an "AS IS" BASIS,			#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.	#
# See the License for the specific language governing permissions and		#
# limitations under the License.											#
#############################################################################

from optparse import OptionParser
from subprocess import call
import ConfigParser
import os.path
import sys

#Home variable for python paths
HOME = os.path.expanduser("~")
ver = "0.1.7"

# This if statement will only fire if poke hasn't been set up on the system yet! If it has this block will be skipped!
if os.path.isfile(HOME + "/.poke/servers.cfg") is False:
	print("Setting up poke on your machine...")
	if os.path.isdir(HOME + "/.poke") is False:
		call("mkdir ~/.poke", shell=True)
		call("chmod -R 766 ~/.poke", shell=True)

	# Because the config doesn't exist yet it needs to be created!
	configWriter = open(HOME + '/.poke/servers.cfg', 'wb+')
	header = ["Server config for poke v%s CLT by Katharina Sabel" % ver, "Email katharina.sabel@2rsoftworks.de suggestions and comments", "Visit support.2rsoftworks.de to report issues", "", "You can add your servers as sections below.", "Each section needs to have the Alias and URL field set but can have another field to determine", "if XTerm should be used for the SSH session.", "Note that the shorthands 'h', '?' and 'x' are reserved by the application.", "", "Name: Define a helpful name for your server", "ShortHand: short command-line argument", "LongHand: long command-line argument", "URL: server address", "User: server user (if needed)", "XDef: Default XTerm settings"]

	body = ["", "[SampleServer]", "Name: Jane's NAS", "ShortHand: j", "LongHand: jane", "URL: 111.222.333.444", "User: Jane", "XDef: False"]

	for item in header:
		if item == "":
			configWriter.write(item + "\n")
		else:
			configWriter.write("# " + item + "\n")
	for item in body:
		configWriter.write(item + "\n")
	configWriter.close()

	print "\nSuccessfully wrote 'server.cfg'. You should probably go to ~/.poke/ and set up your servers!\n"
	introParser = OptionParser()
	introParser.add_option("-?", action="store_false", help="Open 'Nano' to editor your server config")
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

def runNaNo(option, opt_str, value, parser):
	call("nano %s/.poke/servers.cfg" % HOME, shell=True)

# Options Paser
parser = OptionParser(version="%s" % ver)
parser.add_option("-?", action="callback", help="Open 'Nano' to edit your server config file", callback=runNaNo)
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
		return "-x"
	else:
		return ""

if ServerSetupComplete:
	print "Connecting to server %s@%s" % (UserName, ServerURL)
	if prefs.xterm:
		print "Overwriting stored XTerm Settings"
		UseXTerm = True
	call("ssh %s@%s %s" % (UserName, ServerURL, getXTermSetting()), shell=True)