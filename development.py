#!/usr/bin/env python

# Kludge to wrap pip for travis
import os

with open('requirements.txt', 'r') as fh:
    for line in fh:
        os.system("pip install %s" % (line.rstrip()))
