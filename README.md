Ghost in the Shell (ghost)
====

The most annoingly awesome ssh utility in the universe. Contains 25% more ssh than the competition. 

**At this time only `fish` is properly supported. Please check back later for more console support - or open a ticket for your favourite console. Thanks!**

Manage ssh config
-----------------

Managing large ssh configs is annoying. Fiddling around with ssh parameters and then creating a config entry from that is time consuming and boring. And there really should be a tool to automate the process. Now there is!

```bash
$> ssh myuser@182.11.185.23 -D 3182 -X -p 1022
...
ghost mkcfg super_server
```

Ghost will look through your history and take the last successful (and valid) ssh command and create a config from it. Completely automatic. It will even let you know if it thinks the entry already exists (in some shape or form).

And removing an automatically generated config entry is as easy as pie. 

```bash
ghost rm super_server
```

Take your world with you
------------------------

We all have special setups and shortcuts and scripts and...
And then we log into a client machine just to realise that their .vimrc is non-existent and by default `ll` is mapped to `cowsay "The fuck?"`. Now there is a solution to this!

Simply configure ghost with a configuration in which you define what things you want to take with you when working on servers. You can even blacklist servers to NOT take certain things with you. This includes your fishrc, your aliases and even custom scripts from a path of your choosing!

And the best thing? After initial configuration, you don't have to do a thing!

```bash
$> ghost super_server
```

And after you're done all the temporary stuff will be removed from the server again...as if you were never there!

Automatic keys
--------------

Yes...we should all have unique keys for every server. And yes, we should totally change them from time to time. And no, nobody *ever* does so. Because it's time consuming and boring. Until now!

With a simple parameter ghost will not only connect to a server but also check the age of the key on said server. And if the key is too old generate a new one, swap out the public keys, test the key in the background and only after successful connection delete the old keys.

This way you will always be in excellent shape with your key management. With next to zero effort on your behalf!

Isn't that awesome? Naaaah? Naaaaah? C'maaaaaaan!
