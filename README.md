# Poke SSH utility
This is an SSH command-line utility tool designed to connect you to various ssh servers. 

Instead of having to type server connections over and over or use 10 different aliases to do 10 different things you can now use Poke to set up as many SSH connections as you want and use them all with just one command.

When running Poke for the first time the tool will create a few configuration files at ```~/.poke/```. One is a global configuration file that contains the config and user path as well as version and OS information.

In addition to that two more configuration files are created. One called ```~/.poke/servers.cfg*``` and the other called ```~/.poke/keys.cfg```.

The server configuration uses a standard configuration layout:

| Section  | Effect |
| ------------- | ------------- |
| [Section Name]  | Has no effect on functionality. Only for your convenience |
| Name (Optional) | Nickname for your server. Will be displayed in the server list |
| ShortHand  | Single character to address the section. Used to address the server. |
| LongHand (Optional) | String to address the section. Used to address the server. |
| URL  | Server address as IP or Domain.  |
| User  | SSH username on the remote machine.  |
| XDef (Optional)  | Boolean to indicate default ```-X``` setting on SSH session.  |
| Key (Optional) | Specifies a key in the keys.cfg file to use instead of a password authentication  |

The ```~/.poke/keys.cfg``` has a simmilar layout to add keys. SSH keys are stored at ```~/.ssh``` by default however the location can be overwritten in the global configuration file. For examples of that check the ```samples/global``` file

The key configuration file acts as follows:

| Section  | Effect |
| ------------- | ------------- |
| [Section Name]  | Has no effect on functionality. Only for your convenience |
| ID | ID-String for the SSH Key|
| ShortID  | Single character to address the key |
| Path | Name of the actual key-file in your ssh directory. Note that the path can be changed in the Poke configuration. Check the sample section for details. |
| Access (Optional) (**Experiental**)  | Determines the access level of the user on the remote server to determine before-hand if an opration can be run or not. 0 is root, 1 is the default user. Add additional values as you need them.  |

For more examples on how to configure your keys check the ```samples/keys.cfg```file

**Note: You need to have ssh installed for poke to work**.

If you have issues using Poke check the Issue Tracker on this repository. If none exists already, please create one so I can get back to you.
