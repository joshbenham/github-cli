# import oauth2 as oauth
import urllib
import requests
import json
import sys
from github_cli.config import Config

class Github:
    """Represents an authenticated session to github"""
    def __init__(self, base):
        self.base = base

        self.feeds = {}
        mod = sys.modules[__name__]
        for name in dir(mod):
            attr = getattr(mod, name)
            if GithubFeed in getattr(attr, '__bases__', []):
                self.feeds[name.lower()] = attr

    def __getattr__(self, attr):
        if attr in self.feeds:
            return self.feeds[attr](self.base)
        else:
            super(self)


class GithubFeed:
    """Represents a single item in github's API.
    Baseclass only"""
    def __init__(self, base):
        self.base = base
        self.config = Config()
        pass

    def __call__(self, *args, **kwargs):
        """Used to make feed accessors"""
        raise NotImplementedError


class Issues(GithubFeed):
    def __init__(self, *args):
        GithubFeed.__init__(self, *args)
        self.url = "%(base)s/issues" % { "base": self.base }

    def __call__(self, params):

        try:
            url = "%(base)s/repos/%(user)s/%(repo)s/issues" % { "base": self.base, "user": params['user'], "repo": params["repo"] }
        except KeyError:
            url = self.url

        del params['user']
        del params['repo']

        data = {"url": url,
                "params": urllib.urlencode(params)
               }
        resp = requests.get("%(url)s?%(params)s" % data, auth=(self.config["username"], self.config["password"]))
        return json.loads(resp.text)

