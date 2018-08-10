# 👉🏽 poke [![](https://travis-ci.org/spacekookie/poke.svg?branch=master)](https://travis-ci.org/spacekookie/poke) [![](https://ci.appveyor.com/api/projects/status/w29yfx0q5kls3013?svg=true)](https://ci.appveyor.com/project/spacekookie/poke)

A password manager for your keys; a key manager for your soul.

## What?

Private ssh-keys are kinda broken. Because of this, poke attempts to circument the problems by storing keys in a different format, encrypted in a [lockchain]() keystore. You can create new keys and store them directly in this store with the `poke` cli.

`poked` is an ssh-agent daemon which serves unencrypted keys from the keystore. Each key is never held in memory for longer than the operation it is required for.

After unlocking `poked`, use a yubikey to re-encrypt the primary key for re-use
