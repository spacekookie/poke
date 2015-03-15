"""
Poke - SSH Connection Utility

Module: PokeController
============
Manages Poke actions on servers

:copyright: (c) 2014-2015 Katharina Sabel
:license: GPLv3 (See LICENSE)
"""

from subprocess import call, CalledProcessError
import types


class PokeController:

	def __init__(self):
		pass

	def set_servers(self, servers):
		self.servers = servers

	def connect(self, master, field, sub, data):
		if field == None:
			print "You must specify a server first!"
			exit()

		params = ""

		if '--cmd' in sub:
			params += " " + data['--cmd'] + " "
		if '-X' in sub:
			params += " -X "

		user = self.servers[field[0]]['user']
		cmd = "ssh " + user + '@' + field[1][0]
		assemble = cmd + params
		print "==>", "Connecting to", field[0], "with", params.strip()

		# And now actually call the function!
		call(assemble, shell=True)

	def error_handle(self, master, msg):
		if isinstance(master, list):
			master = ' '.join(master)
		print "'%s'" % master, "wasn't understood because:", msg
		pass

	def copy(self, master, field, sub, data):
		if field == None:
			print "You must specify a server first"
			exit()

		file = ''
		target = '~/'
		user = self.servers[field[0]]['user']

		if '--file' in sub:
			file += " " + data['--file']

		if '--target' in sub:
			target += data['--target']

		assemble = "scp" + file + " " + user + "@" + field[1][0] + ":" + target
		call(assemble, shell=True)

	def mount(self, master, field, sub, data):

		if 'mount' in self.servers[field[0]]:
			serv = self.servers[field[0]]['mount']
		else:
			print "No mount target set up"
			exit()

		remote =  serv['remote']
		local =  serv['local']
		user = self.servers[field[0]]['user']
		url = self.servers[field[0]]['url']

		assemble = "sshfs " + user + "@" + url + ":" + remote + " " + local
		call(assemble, shell=True)