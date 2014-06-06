#!/usr/bin/python

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