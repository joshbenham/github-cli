#!/usr/bin/env python

# Kludge to wrap pip for travis

with open('requirements.txt', 'r') as fh:
    for line in fh:
        system("pip install %s" % (line.rstrip()))
