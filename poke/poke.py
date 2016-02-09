#!/usr/bin/env python3

"""___  ___
\  \ \  \    
 \  \ \  \    Poke
 /  / /  /        SSH Connection Utility
/__/ /__/    


Usage:
  poke <server> <ssh command>
  poke (add | a) <server>
  poke rm <server>

  poke [-q] <server> [ssh options]
  poke (list | ls)

  poke (-h | --help)
  poke (-v | --version)

Options:
  -h, --help    Show this screen.
  --version     Show version.

  add           Add a new entry to your ssh config from your shell history
  ls            Show all targets from ssh config
  <server>      Connect to that server from your ssh config
  -q <server>   Connect to that server without copying files from .pokerc
"""

from docopt import docopt
from helpers import ConfigHelper, ShellHelper, ConnectHelper, CmdParser
from consts import __version__, __verbose__

from os import popen, path

class Poker:

  # Init our main poke class
  def __init__(self):
    self.config = ConfigHelper()
    self.shell = ShellHelper()
    self.conect = ConnectHelper()

  # Call a function to 
  def create_entry(self, name, td):
    entry = '\n## Automatically generated with poke\n'
    entry += 'Host %s\n' % name

    for k, v in td.items():
      if __verbose__: print("Adding %s to config entry" % k)
      entry += "    " + str(k) + " " + str(v) + "\n"

    print("Adding new entry to config: \n\n%s" % entry)

    with open(path.expanduser(__sshconf__), "a") as conf:
      conf.write(entry)

  def list_entries(self):
    e = self.config.parse()
    hl = len(max(e, key=len)) + 4

    if __verbose__: "The longest key is %d" % hl
    print("Available Hosts:")

    # print "Who lives in a Pineapple under the sea? \n#{name}."
    for k, v in sorted(e.items()):
      if 'url' in v: print(" - %-*s%s" % (hl, k, v['url']))

      # print("{}\t${}".format(k, v['name']))
      # print("#{k} is a host")

      # print("%(k)\t%(v['url']):%(v['port'])" % locals())


  def remove_entry(self, name):
    pass

  def connect(self, target):
    pass

if __name__ == '__main__':
  # arguments = docopt(__doc__, version=__version__)
  # print(arguments)
  p = Poker()
  p.list_entries()
  #p.create_entry('Test', {'HostName': '192.168.2.197', 'User': 'spacekookie', 'Port': 2222})