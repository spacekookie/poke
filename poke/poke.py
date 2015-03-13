#!/usr/bin/python

"""
Poke - SSH Connection Utility

Application
============

:copyright: (c) 2015 Katharina Sabel
:license: GPLv3 (See LICENSE)
"""


# Controller module imports
from controllers import server_controller as sc
from controllers import poke_controller as p_con

# System requirements
import sys

# Trying import the options parser
# try:
# 	from advoptparse import parser as aop

# # Include local building dependency
# except ImportError:
# sys.path.append('../../AdvOptParse/advoptparse/')
from advoptparse import parser as aop

class Poke:

	def __init__(self):
		self.pc = p_con.PokeController()

		# Create parser objects with the master level commands
		self.p = aop.AdvOptParse(
		{
			'connect':(self.pc.connect, 'Connect to remote servers via ssh'),
			'copy':(self.pc.copy, 'Copy files to remote servers via scp'),
			# 'push':(self.pc.push, 'Push commands directly to remote servers'),
			'mount':(self.pc.push, 'Mount remote server (with config) via sshfs')
		})

		# Define Names and failsafe functions
		self.p.set_container_name('poke')
		self.p.set_fields_name('Servers')
		self.p.register_failsafe(self.pc.error_handle)
		self.p.set_hidden_subs(True)


		# Define aliases for master fields
		self.p.set_master_aliases('connect', ['c'])
		self.p.set_master_aliases('copy', ['cp'])
		# self.p.set_master_aliases('push', ['p'])
		self.p.set_master_aliases('mount', ['m'])

		self.p.set_master_fields('connect', True)
		self.p.set_master_fields('copy', True)
		# self.p.set_master_fields('push', True)
		self.p.set_master_fields('mount', True)

		self.p.add_suboptions('connect', {
			'-X': (None, aop.__VALUE__, "Enable X forwarding for the current session (if not enabled by default)"),
			'--cmd': (None, aop.__FIELD__, "Push a command to a remote server")
		})

		self.p.add_suboptions('copy', {
			'--file': (None, aop.__FIELD__, "Determine an input file to be transfered"),
			'--target': (None, aop.__FIELD__, "Determine the target location on a remote server")
		})

		self.p.define_fields({})


		self.p.help_screen()


	def run(self, args):
		pass # print ""



if __name__ == "__main__":
	poke = Poke()
	poke.run(sys.argv[1:])
