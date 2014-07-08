class VersionController:
	pass
	
	def __init__(self, url, skeleton):
		self.url = url
		self.skeleton = skeleton

	def fetch(self):
		req = urllib2.Request(self.url)
		opener = urllib2.build_opener()
		f = opener.open(req)
		jdata = json.load(f)
