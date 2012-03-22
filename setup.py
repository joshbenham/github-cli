import os
import sys
from setuptools import setup

setup(name='github_cli',
	version='0.1',
	description='Command Line Interface for GitHub',
	long_description=open('README.md').read(),
	classifiers=[
		"Programming Language :: Python",
	],
	author="Josh Benham",
	author_email='joshbenham@gmail.com',
	url='https://github.com/joshbenham/github-cli',
	keywords='web python github git cli',
	packages=['github_cli',],
	scripts=['github'],
	install_requires=open('requirements.txt').read(),
)

