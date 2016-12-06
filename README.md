![Poke Logo](https://raw.githubusercontent.com/spacekookie/ssh-poke/master/shell_sc_313.png)

The most annoyingly awesome, most powerful and all knowing [ssh][ssh] host and key manager written in C with [libssh][libssh] and [libdyntree][libdyntree]. Contains 25% more ssh than the leading competitor^1^.


## How to use

poke works by augmenting your default `ssh config`. Traditionally, you could create sections to add hosts, and attach information to them so that ssh knows how to connect to them. Poke makes this easier.

**Adding new hosts**

You can either add a new host directly (explicitly):

```console
user@machine ~ $> poke -add testserv megauser@33.44.55.66 -D 3182 -X -p 9001
```

or you can add a new host implicitly by looking at your previous ssh commands and picking the last one from the list:

```console
user@machine ~ $> ssh megauser@33.44.55.66 -D 3182 -X -p 9001
user@machine ~ $> poke --add testserv
```

**Listing all known hosts**

If you just quickly want to get an overview of what hosts you have setup in your config you can simply use the list command:

```console
user@machine ~ $> poke --list
 - server1 (5.1.1.244)
 - uni3 (server.uit-university.edu)
 - jane.nas (192.168.1.22)
```

**Connecting to a host**

You can use poke to connect to your hosts while letting it also handle a few very useful things in the background for you. This means that all your key-rules can be enforced during connection time (details see below)

```console
user@machine ~ $> poke jane.nas
[Key Update] Your key was updated because it was 32.4 days old!

Host key fingerprint is f9:63:1a:22:9f:d4:00:11:1f:bc:de:fa:dc:ec:2b:47
+----[SHA 256]----+
|                 |
|                 |
|                 |
|      .   .      |
|      . o  .     |
|       . S  E    |
|      .   * .    |
|       .= +X.    |
|        .=EBO.   |
+-----------------+

Last login: Sat Nov  18 00:00:00 1995 from 0.0.0.0
guest@jane.nas ~ $>
```

#### Automatic keys

Yes, we should all have unique keys for every server we connect to. And yes, we should exchange those keys as frequently as possible. But nobody *ever* does. Because it takes a lot of time and is boring. And we just forget.

Poke can help! When using `poke ` to connect to a server, it will by default check the key that is being used to connect. If the key doesn't exist, it will create one. If it is too old, it will exchange it. Always making sure that you are safe. You don't need to do anything!

If you don't want to use poke as an SSH agent, don't worry. You can start `poked`, the poke daemon. It runs in the background of your system and periodically checks the age of keys and exchanges them if required.

## How to build

Poke can be built with `cmake`.Make sure that you have access to both libssh-dev and libdyntree-dev. The latter is included in the main repository via a git submodule. Thus, make sure to fetch it during cloning

```console
$> git clone --recursive https://github.com/spacekookie/poke.git
```

An out of source build is recommended with cmake:

```console
$> mkdir build && cd build
$> cmake ..
$> make
```


## Installation

Installing can be done by simpling typing `sudo make install`. This should only be done if poke can't be installed via a global package manager system.

There is a pre-built `poke` package on the [AUR][aur_package]

## Miscellanious

Poke is published under the GPL-3 license while libpoke (the library powering the CLI and daemon) is licensed under the LGPL-3 license. This means that you are allowed to embed the library into proprietary work.

If you find any bugs in the code please submit them to the issue tracker in the github repository.

---

~^1^ Tested in a closed environment with a triple blind control group. Study conditions may apply. Your enjoyment in the tool may vary.~

[rustlang]: http://rustlang.org/
[ssh]: https://wikipedia.org/wiki/Secure_Shell
[libssh]: https://wikipedia.org/wiki/Secure_Shell
[libdyntree]: https://wikipedia.org/wiki/Secure_Shell
[aur_package]: https://wikipedia.org/wiki/Secure_Shell
