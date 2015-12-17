#!/usr/bin/env python

# This is the help screen
"""
"""

# Now make the help screen
import docopt

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
  p = Poker()