from consts import __verbose__
from os import popen, path

class ConfigHelper:

  def __init__(self):
    self.__sshconf__ = '~/.ssh/config'

  def parse(self):
    val = popen("cat %s | grep -v '#'" % path.expanduser(self.__sshconf__))
    entries = {}
    buff = {}

    ''' 
    Host <...>
      HostName <...>
      User <...>
      Port <...>
      IdentitiesOnly <...>
      IdentityFile <...>
    '''

    # Go over the config line by line
    for tbs in val.readlines():
      line = tbs.strip()
      if line == '': continue

      if line.startswith('HostName'):
        buff['url'] = line[9:].strip()
      
      elif line.startswith('Host'):

        if buff != {}:
          entries[buff['name']] = buff
          buff = {}
        buff['name'] = line[5:].strip()

      elif line.startswith('Port'):
        buff['port'] = int(line[5:].strip())

      elif line.startswith('IdentitiesOnly'):
        res = line[15:].strip()

        if res == 'yes': buff['id_o'] = True
        else: buff['id_o'] = False

      elif line.startswith('IdentityFile'):
        buff['id_f'] = line[13:].strip()

      elif line.startswith('#poke='):
        pass # This is where our inline config would be read in!

    # Then return our entry set for formatting
    return entries

class ShellHelper:
  '''
  # TODO: Implement all of these

  However, if the executable is not matching real shell (e.g. /bin/sh is actually bash or ksh), you need heuristics. Here are some environmental variables specific to various shells:

    $version is set on tcsh

    $BASH is set on bash

    $shell (lowercase) is set to actual shell name in csh or tcsh

    $ZSH_NAME is set on zsh

    ksh has $PS3 and $PS4 set, whereas normal Bourne shell (sh) only has $PS1 and $PS2 set. This generally seems like the hardest to distinguish - the ONLY difference in entire set of envionmental variables between sh and ksh we have installed on Solaris boxen is $ERRNO, $FCEDIT, $LINENO, $PPID, $PS3, $PS4, $RANDOM, $SECONDS, $TMOUT.
  '''

  def __init__(self):
    val = popen("echo $SHELL")
    self.shell = val.readlines()[0].split('/')[-1].strip()
    if __verbose__: print("Found shell to be", self.shell)

    if self.shell == 'fish':
      self.history = path.expanduser('~/.config/fish/fish_history')
    else:
      print('Sorry, your shell is not supported by poke! :(')
      exit(-1)

    if __verbose__: print('History path is', self.history)


class ConnectHelper:
  pass

class CmdParser:
  pass
