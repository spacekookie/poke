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

class Strings():

	def __init__(self, version):
		self.serverHead = ["Server config with Poke v%s by Katharina Sabel (Updates may cause incompatibility)" % version, "Email katharina.sabel@2rsoftworks.de suggestions and comments", "Visit 'https://github.com/SpaceKookie/Poke' to report issues", "", "You can add your servers as sections below.", "The minimum amount of data per server is a handle, a URL and a user.", "XTerm and SSH-Keys are 'False' by default and need to be overwritten", "Note that the shorthands 'h', '?', 'K' and 'X' are reserved by the application.", "","[Section]; Name not important", "Name: Name string for your convenience", "ShortHand: single character handle", "LongHand: multi-character handle", "URL: Server address as IP or Domain", "User: SSH Username", "XDef: True/ False to use XTerm by default", "Key: Set a default SSH key (look into keys.cfg for info)"]

		self.serverBody = ["[HomeServer]", "Name: Jane's NAS", "ShortHand: j", "LongHand: jane", "URL: 111.222.333.444", "User: Jane", "Key: default", "", "[Work Server]", "Name: Work Cluster", "ShortHand: w", "LongHand: work", "URL: workserver.kiwi", "User: employee1337", "XDef: True", "Key: work"]
		self.keyHead = ["SSH Key config for Poke v%s by Katharina Sabel" % version, "Email katharina.sabel@2rsoftworks.de suggestions and comments","Visit support.2rsoftworks.de to report issues", "", "You can add your private SSH keys down below", "Each section needs to have an ID field, the path and access priority", "Note that you can enter any ID combination you want.", "Check the github wiki for more information"]
		self.keyBody = ["[Key1]", "ID: default", "ShortID: def", "Path: id_rsa", "Access: 3", "", "[Key2]", "ID: work-key", "ShortID: wk", "Path: work_id", "Access: 0"]

		self.globalHead = ["This file contains important information to run Poke", "Do not change anything unless you know what you're doing!", "In case of corruption remove this file to re-init"]
		
class CCodes():

	def __init__(self):
		self.HEADER = "\033[95m"
		self.OKBLUE = "\033[94m"
		self.OKGREEN = "\033[92m"
		self.WARNING = "\033[93m"
		self.FAIL = "\033[91m"
		self.ENDC = "\033[0m"

class PurgeDiag:

	def __init__(self):
		self.init_head = "==> YOU ARE ABOUT TO PURGE POKE FROM YOUR SYSTEM !!!\n"
		self.init_check = "I will need root privileges to remove Poke correctly. Continue? [Y/n]: "
		self.init_canceled = "==> PURGE CANCELED"
