# 👉🏽 point poke [![](https://travis-ci.org/spacekookie/poke.svg?branch=master)](https://travis-ci.org/spacekookie/poke) [![](https://ci.appveyor.com/api/projects/status/w29yfx0q5kls3013?svg=true)](https://ci.appveyor.com/project/spacekookie/poke)

A conveniently easy to use ssh key generator and manager.

## Usage

```console
$ poke generate beast
Generating public/private ed25519 key pair.
Your identification has been saved in /home/spacekookie/.ssh/poke/azedes_beast.
Your public key has been saved in /home/spacekookie/.ssh/poke/azedes_beast.pub.
The key fingerprint is:
SHA256:5Y85WJDLBKkMnQmLlZpmv5X33okAJ6lw6oMRmiofxfU spacekookie@azedes
The key's randomart image is:
+--[ED25519 256]--+
|  o+ o..         |
| oo.+ .. .       |
|.o.o .. + .      |
|+o .o..+ =       |
|++..o+..E o      |
|+ +o.o+. o +     |
|oo..o ..o + .    |
|=. o    ..o..    |
|.oo     .o o     |
+----[SHA256]-----+

Your server address: 1.22.333.44
Adding public key to server.........................................DONE
You can now connect without password with `ssh beast`
```

