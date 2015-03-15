#!/usr/bin/python

"""
Poke Config Manager - Manage Poke configurations

Application
============

:copyright: (c) 2014-2015 Katharina Sabel
:license: GPLv3 (See LICENSE)
"""

# SpaceKookie imports
from controllers.server_controller import ServerController
from advoptparse import parser as p # Hope this is installed!

# System imports
import version
import getpass
import sys

__USER__ = getpass.getuser()
__PORT__ = 22

class PokeConfigManager:

	def __init__(self):
		if "linux" in sys.platform:
			self.sc = ServerController('linux')
		else:
			self.sc = ServerController('osx')

		self.parser = p.AdvOptParse({
			'add-server':(self.handle, "Add poke remote server"),
			'rm-server':(self.handle, "Remove poke remote server"),

			'add-mount':(self.handle, "Add mountpoint for remote server"),
			'rm-mount':(self.handle, "Remove mountpoint for remote server"),

			'add-copy':(self.handle, "Add copy task for remote server"),
			'rm-copy':(self.handle, "Remove copy task for remote server")
		})

		self.parser.set_container_name('poke-config-manager')
		self.parser.set_fields_name('Functions')	
		# self.parser.register_failsafe(self.pc.error_handle)
		# self.parser.set_hidden_subs(True)
		self.parser.set_help_handle(False)
		self.parser.set_version_handle(False)

		# self.parser.set_master_fields('server', True)
		# self.parser.set_master_fields('function', True)

		self.parser.add_suboptions('add-server', {
			'--name': (None, p.__FIELD__, ""),
			'--url': (None, p.__FIELD__, ""),
			'--note': (None, p.__FIELD__, "(default: <name of server> remote server)"),
			'--port': (22, p.__FIELD__, "(default: " + str(__PORT__) + ")"),
			'--user': (None, p.__FIELD__, "(default: " + __USER__ + ")"),
		})

		self.parser.add_suboptions('rm-server', {
			'--name': (None, p.__FIELD__, "Name of the server to be removed")
		})

		self.parser.add_suboptions('add-mount', {
			'--name': (None, p.__FIELD__, "Specify a server to add this function to"),
			'--remote': (None, p.__FIELD__, "(default: ~/)"),
			'--local': (22, p.__FIELD__, "(default: /mnt/<name of server>)"),
			'--user': (None, p.__FIELD__, "(default: " + __USER__ + ")"),
		})

		self.parser.add_suboptions('rm-mount', {
			'--name': (None, p.__FIELD__, "Specify a server to remove this function from"),
		})

		self.parser.add_suboptions('add-copy', {
			'--name': (None, p.__FIELD__, "Specify a server to add this function to"),
			'--remote': (None, p.__FIELD__, "(default: ~/)"),
			'--user': (None, p.__FIELD__, "(default: " + getpass.getuser() + ")"),
		})

		self.parser.add_suboptions('rm-copy', {
			'--name': (None, p.__FIELD__, "Specify a server to remove this function from"),
		})

		# self.parser.help_screen()

	def run(self, args):
		new_args = []
		for e in args:
			if " " in e:
				e = e.replace('=', '="')
				e += '"'
			new_args.append(e)

		if args == []:
			self.parser.help_screen()
		else:
			self.parser.parse(' '.join(new_args))

	def handle(self, master, field, sub, data):
		if master == "add-server":
			if '--port' not in data:
				data['--port'] = __PORT__

			if '--note' not in data:
				data['--note'] = data['--name'] + ' remote server'

			if '--user' not in data:
				data['--user'] = __USER__

			self.sc.add_server(data['--name'], data['--user'], data['--url'], data['--note'], data['--port'])
		elif master == "rm-server":
			self.sc.add_server(data['--name'])

		elif master == "add-mount":
			if '--user' not in data: data['--user'] = __USER__
			if '--local' not in data: data['--local'] = '/mnt/' + data['--name']

			self.sc.add_server_function(data['--name'], 'mount', {'remote': data['--remote'], 'local': data['--local'], 'user': data['--user']}, False)
		elif master == "rm-mount":
			self.sc.remove_server_function(self, data['--name'], 'mount')
		elif master == "add-copy":
			self.sc.add_server_function(data['--name'], 'copy', {'remote': data['--remote'], 'user': data['--user']}, False)
		elif master == "rm-copy":
			self.sc.remove_server_function(data['--name'], 'copy')
		else:
			self.parser.help_screen()

def run():
	pcm = PokeConfigManager()
	pcm.run(sys.argv[1:])	

if __name__ == "__main__":
	pcm = PokeConfigManager()
	pcm.run(sys.argv[1:])