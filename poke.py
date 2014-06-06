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

from Controllers import SessionController
from Controllers import KeyHostController
from datetime import datetime
from os import path
from Intro import Setup
import Poke

# This is the main application file and entry point for the Poke commandline tool.
class Poke():

	# Self variables
	home = path.expanduser("~") # Change this to move Poke-location (not recomended)
	version = "0.3.2"
	workingDirectory = ".poke" # Change this to rename working directory
	access = 1 # if 0: root is required to write/ read ssh/ servers

	def main(self):
		# Creates a starter object to init default values. If already set these will be read from config
		start = Setup(self.home, self.version, self.workingDirectory)
		start.make()


	# Starts the application
	if __name__ == "__main__":
		startTime = datetime.now()
		Poke.Poke().main()
		print(datetime.now()-startTime)


#session = SessionController("r2soft.de", "katharina", None)
#session.callServer() '''