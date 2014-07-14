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

''' This class handles the conversion of .ini configs to JSON configs ''' 

from sys import exit
import json as js


class ConversionController:

	def __init__(self, working_directory, old_version, target_version):
		self.working_directory = working_directory
		self.old_version = old_version
		self.target_version = target_version
		response = raw_input("Upgrading from %s to %s. Is that correct?" % (self.old_version, self.target_version))
		if response.lower() == "y" or response.lower() == "":
			pass
			# Go on with stuff here
		else:
			# Print something here
			exit()


	pass