import os
import sys

import github_cli.config
from github_cli.github import Github

from github_cli.message_parser import MessageParser

class NoTitleError(Exception): pass

def we_are_tty():
    for i in sys.stdin, sys.stdout, sys.stderr:
        if not os.isatty(i.fileno()):
            return False
    return True

class PullRequests:

    def __init__(self, args):
        self.args = args
        self.messageparser = MessageParser()

    def get_title(self):
        if self.args.title:
            return self.args.title[0]
        elif we_are_tty():
            return self.messageparser.get_title()
        else:
            raise NoTitleError

    def get_message(self):
        if self.args.message:
            return self.args.message[0]
        elif we_are_tty():
            return self.messageparser.get_message()
        else:
            raise NoMessageError

    def get_head(self):
        if self.args.head:
            return self.args.head
        # Try to work out what branch we're on somehow

    def execute(self):
        params = {}

        params['pull[base]'] = self.args.base

        params['pull[head]'] = self.get_head()

        params['pull[title]'] = self.get_title()

        params['pull[body]'] = self.get_message()

        print(params)
