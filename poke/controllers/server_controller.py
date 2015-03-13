"""
Poke - SSH Connection Utility

Module: ServerController
============
Manages server configuration files

contains:
	add_server(name, url)

	remove_server(name)

	add_server_function(server_name, function_type, function_data)

	remove_server_function(server_name, function_type)

:copyright: (c) 2015 Katharina Sabel
:license: GPLv3 (See LICENSE)
"""

import pickle
import os

__SERVER__ = '.server'

class ServerController:

	def __init__(self, user_os):
		# self.path = ""
		if user_os == "linux":
			self.path = os.path.expanduser('~') + '/.config/poke/'
		elif os == 'osx':
			self.path = os.path.expanduser('~') +'~/Library/poke'

		if not os.path.exists(self.path):
			os.makedirs(self.path, 0700)
			print "New config directory created. Use 'poke-config-manager' to add servers now."

	def add_server(self, name, url, port = 22):
		server = {}
		server['name'] = name
		server['url'] = url
		server['port'] = port

		print "This is a new server: ", server 

		tmp_file = self.path + name + __SERVER__
		if not os.path.exists(tmp_file):
			pickle.dump(server, open(tmp_file, 'wb+'))
			os.chmod(tmp_file, 0600)
		else:
			print "Server", name, "already exists. Please update it instead."

	def remove_server(self, name):
		tmp_file = self.path + name + __SERVER__
		if os.path.exists(tmp_file):
			os.remove(tmp_file)

	def add_server_function(self, server_name, function_type, function_data, force = False):
		tmp_file = self.path + server_name + __SERVER__
		if not  os.path.exists(tmp_file):
			print "Server doesn't yet exist. Create it first with 'poke-config-manager add <server>'"
			return
		
		server = pickle.load(open(tmp_file, 'rb'))

		if function_type not in server or force:
			server[function_type] = function_data
		else:
			print "Function already registered. Use -f to overwrite."

		pickle.dump(server, open(tmp_file, 'wb+'))

	def remove_server_function(self, server_name, function_type):
		tmp_file = self.path + server_name + __SERVER__

		if not  os.path.exists(tmp_file):
			print "Server doesn't yet exist. Create it first with 'poke-config-manager add <server>'"
			return

		server = pickle.load(open(tmp_file, 'rb'))

		if function_type in server:
			server.pop(function_type, None)
			pickle.dump(server, open(tmp_file, 'wb+'))
		else:
			print "Function didn't exist. Server file kept unchanged."

	def show_server(self, server):
		tmp_file = self.path + server + __SERVER__
		print pickle.load(open(tmp_file, 'rb'))

