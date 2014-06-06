#!/usr/bin/python

class Servers:

	def __init__(self):
		pass

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