# Poke SSH utility
This is an SSH command-line utility tool designed to connect you to various ssh servers. 

Instead of having to type server connections over and over or use 10 different aliases to do 10 different things you can now use Poke to set up as many SSH connections as you want and use them all with just one command.

When running Poke for the first time the tool will create a few configuration files at *~/.poke/*. One is a global configuration file that contains the config and user path as well as version and OS information.

In addition to that two more configuration files are created. One called *~/.poke/servers.cfg* and the other called *~/.poke/keys.cfg*.

The server configuration uses a standard configuration layout:

*[Section Name]
Name: Nickname for the server
ShortHand: Single character to address the section
LongHand: String to address the section
URL: Server address as IP or Domain
User: SSH username on the remote machine
XDef: Boolean to indicate default "-X" setting on SSH session
Key: Specifies a key in the keys.cfg file to use instead of a password authentication*

The *~/.poke/keys.cfg* has a simmilar layout to add keys. SSH keys are stored at *~/.ssh* by default however the location can be overwritten in the global configuration file.


**Note: You need to have ssh installed for poke to work**.

Planned functionality is to copy and move files to and between servers as well.
