#!/usr/bin/python

from subprocess import call

print("This script will quickly compile poke on your system. If this fails...tough luck!")
print("Check github for help")
print("Work in progress: please make an alias of 'makespec.py' from Pyinstaller to pmake. This will be implemented properly at a later time. This script will fail otherwise!!!")

call("pmake -n poke -F source/*", shell=True)
call("pyinstaller poke.spec")

print("You should now have a freshly baked poke binary in the dist/ folder. Huzza")