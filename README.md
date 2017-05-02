![Poke Logo](shell_sc_313.png)

`poke` is the most anoyingly awesome, most powerful and most extendable [ssh][ssh] host and key manager written in C. It contains 25% more SSH than the leading competitor.

## Usage

Hosts are stored in your ~/.ssh/config file and can be added in one of two ways. Explicitly:

```console
user@machine ~ $> poke my_server myuser@182.11.185.23 -D 3182 -X -p 1022
```

or implicitly by crawling through your shell history:

```console
user@machine ~ $> ssh myuser@182.11.185.23 -D 3182 -X -p 1022
user@machine ~ $> poke add my_server
```

Some other useful commands

```console
user@machine ~ $> poke ls
* super_server
* uni3
* jane.nas

user@machine ~ $> poke rm super_server

user@machine ~ $> poke jane.nas
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

## Now in depth

For people who actually care (this is all in alpha anyways :) )

#### Take your world with you

We all have special setups and shortcuts and scripts and...
And then we log into a client machine just to realise that their .vimrc is non-existent and by default `ll` is mapped to `cowsay "The fuck?"`. Now there is a solution to this!

Simply configure poke with a configuration in which you define what things you want to take with you when working on servers. You can even blacklist servers to NOT take certain things with you. This includes your fishrc, your aliases and even custom scripts from a path of your choosing!

And the best thing? After initial configuration, you don't have to do a thing!

```bash
$> poke super_server
```

And after you're done all the temporary stuff will be removed from the server again...as if you were never there!

#### Automatic keys

Yes...we should all have unique keys for every server. And yes, we should totally change them from time to time. And no, nobody *ever* does so. Because it's time consuming and boring. Until now!

With a simple parameter poke will not only connect to a server but also check the age of the key on said server. And if the key is too old generate a new one, swap out the public keys, test the key in the background and only after successful connection delete the old keys.

This way you will always be in excellent shape with your key management. With next to zero effort on your behalf!

Isn't that awesome? Naaaah? Naaaaah? C'maaaaaaan!


## Tests

Yes yes, I'll write tests. I promise

## Installation

Whatever...

[rustlang]: http://rustlang.org/
[ssh]: https://wikipedia.org/wiki/Secure_Shell
=======
