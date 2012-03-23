import sys
from argparse import ArgumentParser

from github_cli import actions
actions.actions = {} #{{{
# XXX Code smell
from github_cli.actions import config
actions.actions['Config'] = config.Config
from github_cli.actions import issues
actions.actions['Issues'] = issues.Issues
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
		arg('--user', default=False, nargs=1, help='List the issues for a particular user', action='store'),
        arg('--repo', default=False, nargs=1, help='List the issues for a particular repo', action='store'),
        arg('--filter', default='assigned', nargs=1, help='Filter issues by assigned, created, mentioned or subscribed. Default: assigned', action='store'),
        arg('--labels', nargs=1, help='Filter by comma seperated labels. Example: bug,ui,@high', action='store'),
        arg('--state', default='open', nargs=1, help='Filter state by open or closed. Default: open', action='store'),
        arg('--sort', default='created', nargs=1, help='Filter sort by created, updated or comments. Default: created', action='store'),
        arg('--direction', default='desc', nargs=1, help='Filter direction by asc or desc. Default: desc', action='store'),
    ]

class Config(Command):
    """configure github authentication"""
    args = [
        arg('username', nargs=1, default=None)
    ]
