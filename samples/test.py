#!/usr/bin/python

import yaml
stream = open("servers-enhanced.yaml", 'r')
print yaml.load(stream)