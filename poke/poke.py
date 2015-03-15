#!/usr/bin/python

"""
Poke - SSH Connection Utility

Application
============

:copyright: (c) 2014-2015 Katharina Sabel
:license: GPLv3 (See LICENSE)
"""


# Controller module imports
from controllers.server_controller import ServerController
from controllers.poke_controller import PokeController

# System requirements
import sys

# Trying import the options parser
# try:
# 	from advoptparse import parser as aop

# # Include local building dependency
# except ImportError:
# sys.path.append('../../AdvOptParse/advoptparse/')
from advoptparse import parser as aop

import version

class Poke:

	def __init__(self):
		self.pc = PokeController()

		# Setup the server controller to fetch server setups.
		if "linux" in sys.platform:
			self.sc = ServerController('linux')
		else:
			self.sc = ServerController('osx')

		# Create parser objects with the master level commands
		self.parser = aop.AdvOptParse(
		{
			'connect':(self.pc.connect, 'Connect to remote servers via ssh'),
			'copy':(self.pc.copy, 'Copy files to remote servers via scp'),
			# 'push':(self.pc.push, 'Push commands directly to remote servers'),
			'mount':(self.pc.mount, 'Mount remote server (with config) via sshfs')
		})

		# Define Names and failsafe functions
		self.parser.set_container_name('poke')
		self.parser.set_fields_name('Servers')
		self.parser.set_container_version(version.__version__)
		self.parser.register_failsafe(self.pc.error_handle)
		# self.parser.set_hidden_subs(True)
		self.parser.set_help_handle(False)


		# Define aliases for master fields
		self.parser.set_master_aliases('connect', ['c'])
		self.parser.set_master_aliases('copy', ['cp'])
		# self.parser.set_master_aliases('push', ['p'])
		self.parser.set_master_aliases('mount', ['m'])

		self.parser.set_master_fields('connect', True)
		self.parser.set_master_fields('copy', True)
		# self.parser.set_master_fields('push', True)
		self.parser.set_master_fields('mount', True)

		self.parser.add_suboptions('connect', {
			'-X': (None, aop.__VALUE__, "Enable X forwarding for the current session (if not enabled by default)"),
			'--cmd': (None, aop.__FIELD__, "Push a command to a remote server")
		})

		self.parser.add_suboptions('copy', {
			'--file': (None, aop.__FIELD__, "Determine an input file to be transfered"),
			'--target': (None, aop.__FIELD__, "Determine the target location on a remote server")
		})

		self.build_servers()

	def run(self, args):
		new_args = args
		# for e in args:
		# 	if " " in e:
		# 		e = e.replace('=', '="')
		# 		e += '"'
		# 	new_args.append(e)

		if new_args == []:
			self.parser.help_screen()
		else:
			self.parser.parse(new_args)

	def build_servers(self):
		# This will be coming...soon, ish?
		__YES__ = '[x]'
		__NO__ = '[ ]'

		servers = self.sc.fetch_servers()
		fields = {}

		for key, value in servers.iteritems():
			string = value['url']
			fields[key] = (value['url'], value['note'])

		self.parser.define_fields(fields)
		self.pc.set_servers(servers)


def run():
	poke = Poke()
	poke.run(sys.argv[1:])

if __name__ == "__main__":
	poke = Poke()
	poke.run("mount lilian") #sys.argv[1:]