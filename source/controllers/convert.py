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

from os import environ, pathsep, path, geteuid, popen

class ConvertionController:
	pass

	def __init__(self, home, version):
		self.path = str(home) + "/.poke"
		self.version = version

	# Merges key and server configs
	def merge_documents(self):
		tmpServers = None
		tmpKeys = None

		if path.isdir(self.path):
			if path.isfile(self.path + "/servers.cfg"):
				print "Found servers"
				# tmpServers = open(path + "/servers.cfg")

			if path.isfile(self.path + "/keys.cfg"):
				print "Found keys"
				# tmpKeys = open(path + "/keys.cfg")


cc = ConvertionController("/home/spacekookie", "0.5.0")
print cc.path
print cc.version
cc.merge_documents()