import os

from setuptools import setup

def get_install_requires():
    try:
        if os.environ["PYTHON_ENV"] == "travis":
            return []
    except KeyError:
        pass
    return open('requirements.txt').read()

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
	install_requires=get_install_requires(),
)
