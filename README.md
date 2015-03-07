# Poke SSH utility
This is an SSH command-line utility tool designed to connect you to various ssh servers. 


===
**Poke is currently being designed from scratch with the AdvOptionsParser library here:** https://github.com/SpaceKookie/OptionsPie

**Future versions will have an easier install/ upgrade and workflow process.**
**Version 0.6.0 is currently in the making**

===


// Depreciated:



Instead of having to type server connections over and over or use 10 different aliases to do 10 different things you can now use Poke to set up as many SSH connections as you want and use them all with just one command.

## How to install
You have two options when it comes to installing. You can either stick to one of the snapshop releases that are thoroughly tested and shouldn't contain any bugs. Click on the "releases" tab and download the latest one. In this case you will have to compile the binary file yourself. After downloading and un-tarring the archive with ```tar -xjf poke-x.y.z.tar.bz2``` you run ```./make``` and then ```./make install``` in the 'Poke' directory that was created from the tarball.

Alternatively you can head over to <a href="http://sourceforge.net/projects/poke-ssh-manager/">sourceforge</a> or look under the release section on this repository and download one of the pre-compiled binaries. They are however not even remotely as often updated as the source snapshots and will thus be more developed.

ALTERNATIVELY if you want to help me develop Poke or you're just very masochistic you can download a non-stable snapshot. Non-stable snapshots are mid-release cycle and under heavy development. They will contains bugs and errors. Use at your own disgression. Feedback from those versions can however be very useful to me.

## How to use
After installing poke to your system you can type ```poke``` to list all configured servers (more to that below). Then simply connect to one of the servers by using it's short OR longhandle as a parameter e.g. ```poke --work``` or ``poke -p```.
There are several settings that can be overwritten including the default SSH-Key that will be used for a session and the XTerm configuration for a session.

+ ```poke --work -K default``` will connect to the 'work' server using the 'default' key from the keys.cfg file.
+ ```poke --jane -X``` will connect to the 'jane' server overwriting the XTerm setting to "true" from whatever it was before. You will be notified if it actually changed.

## How to set up
When running Poke for the first time the tool will create a few configuration files at ```~/.poke/```. One is a global configuration file that contains the config and user path as well as version and OS information.

In addition to that two more configuration files are created. One called ```~/.poke/servers.cfg*``` and the other called ```~/.poke/keys.cfg```

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



If you have issues using Poke check the Issue Tracker on this repository. If none exists already, please create one so I can get back to you.
