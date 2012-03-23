import sys
from argparse import ArgumentParser
import actions

actions.actions = {} #{{{
# XXX Code smell
import actions.config
actions.actions['Config'] = actions.config.Config
# import actions.config
# __actions['Issues'] = actions.issues.Issues
#}}}

class Command(object):
    args = []
    def execute(self, args):
        actions.actions[self.__class__.__name__](args).execute()

def arg(*args, **kw):
    return (args, kw)

def commands():
    mod = sys.modules[__name__]
    classes = []
    for attr in [getattr(mod, name) for name in dir(mod)]:
        if Command in getattr(attr, '__bases__', []):
            classes.append(attr)
    return classes

def register_commands(arg_parser):
    cmd_parsers = arg_parser.add_subparsers()
    for cmd in commands():
        _help = (cmd.__doc__ or 'no help').strip().splitlines()[0]
        cmd_parser = cmd_parsers.add_parser(cmd.__name__.lower(), help=_help)
        for (args, kw) in cmd.args:
            cmd_parser.add_argument(*args, **kw)
        cmd_parser.set_defaults(command_class=cmd)

class Issues(Command):
    """list issues"""
    args = [
        arg('repo', default=False, nargs=1, help="List issues form a repo", action="store")
    ]

class Organisations(Command):
    """list organisations"""
    args = [
        arg('-o')
    ]

class Config(Command):
    """configure github authentication"""
    args = [
        arg('username', nargs='?', default=None)
    ]
