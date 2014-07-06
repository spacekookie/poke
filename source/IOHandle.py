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

import json

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

class JSONHandle:

	def __init__(self):
		pass

	def load(self, path):
		pass

	def load_prefedined(self):
		pass

	def strip_json(self, s):
		inCommentSingle = False
		inCommentMulti = False
		inString = False
		 
		t = []
		l = len(s)
		 
		i = 0
		fromIndex = 0
		while i < l:
			c = s[i]
			 
			if not inCommentMulti and not inCommentSingle:
				if c == '"':
					slashes = 0
					for j in xrange(i - 1, 0, -1):
						if s[j] != '\\':
							break
			 
						slashes += 1
			 
					if slashes % 2 == 0:
						inString = not inString
				elif not inString:
					if c == '#':
						inCommentSingle = True
						t.append(s[fromIndex:i])
					elif c == '/' and i + 1 < l:
						cn = s[i + 1]
						if cn == '/':
							inCommentSingle = True
							t.append(s[fromIndex:i])
							i += 1
						elif cn == '*':
							inCommentMulti = True
							t.append(s[fromIndex:i])
							i += 1
			elif inCommentSingle and (c == '\n' or c == '\r'):
				inCommentSingle = False
				fromIndex = i
			 
			elif inCommentMulti and c == '*' and i + 1 < l and s[i + 1] == '/':
				inCommentMulti = False
				i += 1
				fromIndex = i + 1
			 
			i += 1
			 
		if not inCommentSingle and not inCommentMulti:
			t.append(s[fromIndex:len(s)]) 
		return "".join(t)