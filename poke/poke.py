#!/usr/bin/env python

"""___
\  \ 
 \  \ Poke 
 /  /     ssh connection utility
/__/

Usage:
  poke (--mkconf | -c)
  poke <server>
  poke -q <server>
  poke (-h | --help)
  poke --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  <server>      Connect to that server from your ssh config
  -q <server>   Connect to that server without copying files from .pokerc
  --mkconf -c   Add a new entry to your ssh config from your shell history

"""
from docopt import docopt

# Make sure we import all the things we need to namespaces we like
from helpers import ConfigHelper, ShellHelper, ConnectHelper, CmdParser


# Import the version just because YOLO
from version import __version__

class Poker:

  # Init our main poke class
  def __init__(self):
    self.config = ConfigHelper()
    self.shell = ShellHelper()
    self.conect = ConnectHelper()

  # Call a function to 
  def create_entry(self, name, target_data):
    pass

  def remove_entry(self, name):
    pass

  def connect(self, target):
    pass

if __name__ == '__main__':
  arguments = docopt(__doc__, version='0.7.0')
  print(arguments)
  # p = Poker()