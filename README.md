# Poke SSH

The most annoingly awesome ssh utility out there :)

```bash
$> ssh myuser@182.11.185.23 -D 3182 -X -p 1022
...

$> poke mkconf

Enter a name for myuser@182.11.185.23 -D 3182 -X -p 1022
> server1
Done
$> poke server1
...
```

And that's that :) it automatically creates ssh config entries from previous ssh sessions. When ambigous poke will ask you what session to choose from.

### But that is not all

OMG whaaaat? Yea, Poke can do even more.

Have you ever gone to a server and not had your `.vimrc` and it completely drove you insane?

Define files in the `.pokerc` located in `.config/`

```
pre ~/.config/fish/config.fish
pre ~/.vimrc
pre ~/bin/awesome_sauce.sh ~ myscript.sh
```

Then when you connect to a server from your ssh config via poke it will execute the following:

```bash
$> poke server1
$> scp ~/.config/fish/config.fish server1:~/.config/fish/config.fish 
$> scp ~/.vimrc server1:~/.vimrc
$> scp ~/bin/awesome_sauce.sh ~/bin/myscript.sh
$> ssh server1
...
```

Naaaah? Naaaaah? C'maaaaaaan!

Also you can disable that functionality by passing in a parameter to poke:
```
$> poke - server1
...
```