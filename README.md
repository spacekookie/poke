# Poke SSH utility
This is an SSH commandline utility tool designed to connect you to various ssh servers. 

Instead of having to type server connections over and over or use 10 different aliases to do 10 different things you can now use Poke to set up as many SSH connections as you want and use them all with just one command.

When running poke for the first time the tool will create a config file at ~/.poke/servers.cfg. You can either edit that config with an editor of your choice or type "poke -?" to edit it with nano.

Each server needs a new section and a few details set to work:

Name: A nick-name you can give the server for easier recognition.
ShortHand: A single letter to use as a commandline argument (e.g. poke -s).
LongHand: Essentially the same as the Shorthand but the long form, used with "--" (e.g. --standard)
URL: The SSH server address. Can either be IP or domain.
User: The user that you want to use to log-in. It makes sense specifying a user that knows your SSH key so you don't have to enter a password.
XDef: The default value for the "-X" parameter on ssh clients.

Note: You need to have ssh installed for poke to work.

Planned functionality is to copy and move files to and between servers as well.