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

import sys
from subprocess import call

class SessionController:

	def __init__(self, server, user, key):
		self.server = server
		self.user = user
		if key is not None:
			self.key = key
			self.passwd = False
		else:
			self.passwd = True

	def callServer(self):
		print("You are now calling the server. Hurray!")
		call("ssh " + self.user + "@" + self.server, shell=True)

class KeyHostController:

	def __init__(self, key):
		self.key = key

	def useKey(self, key):
		pass