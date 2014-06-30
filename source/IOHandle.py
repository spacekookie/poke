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

class Handle:

	def __init__(self, home):
		self.home = home

	def getSectionMap(self, section, reader):
		value = {}
		options = reader.options(section)
		for opt in options:
			try:
				value[opt] = reader.get(section, opt)
				if value[opt] == -1:
					DebugPrint("skip: %s" % opt)
			except:
				print("Exception caught on %s!" % opt)
				value[opt] = None
		return value

	def getGlobalURL(self, path):
		# Change to use dynamic Key directory
		value = self.home + "/" + ".ssh" + "/" + path
		return value