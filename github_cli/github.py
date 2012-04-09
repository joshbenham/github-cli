OAUTH_SHIM_URL = "http://oauth.psych0.tk/callback/%s"
# import oauth2 as oauth
try:
    import urllib.parse as ul
except ImportError:
    import urllib as ul

import requests
import json
import sys
import github_cli.config

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
        self.config = github_cli.config.Config()
        pass

    def __call__(self, *args, **kwargs):
        """Used to make feed accessors"""
        raise NotImplementedError

class Oauth(GithubFeed):
    def __init__(self, *args):
        GithubFeed.__init__(self, *args)
        self.url = "%(base)s/login/oauth" % { "base": self.base.replace("api.", "") }

    def auth_url(self, id=""):
        params = { "redirect_uri": OAUTH_SHIM_URL % id,
                   "client_id":    github_cli.config.CLIENT_KEY}
        data = {"url": self.url,
                "params": ul.urlencode(params)
               }
        return "%(url)s/authorize?%(params)s" % data

    @staticmethod
    def parse_params(params):
        out = {}
        for k, v in map(lambda n: n.split("="), params.split("&")):
            out[k] = v
        return out

    def __call__(self, path, params):
        data = {"url": self.url,
                "path": path
               }
        resp = requests.post("%(url)s/%(path)s" % data, data=params)
        return self.parse_params(resp.text)

class Issues(GithubFeed):
    def __init__(self, *args):
        GithubFeed.__init__(self, *args)
        self.url = "%(base)s/issues" % { "base": self.base }

    def __call__(self, params):
        try:
            url = "%(base)s/repos/%(user)s/%(repo)s/issues" % { "base": self.base, "user": params['user'], "repo": params["repo"] }
        except KeyError:
            url = self.url

        params["access_token"] = self.config["access_token"]

        data = {"url": url,
                "params": ul.urlencode(params)
               }

        resp = requests.get("%(url)s?%(params)s" % data)
        return json.loads(resp.text)

class NewPullRequest(GithubFeed):
    def __init__(self, *args):
        GithubFeed.__init__(self, *args)
        self.url = "%(base)s/pulls" % { "base": self.base }

    def __call__(self, params):
        url = "%(orig)s/%(repo)s" % { "orig": self.url, "repo": params.pop("repo") }

        rep = requests.post(url, params)
        return json.loads(resp.text)

class PullRequests(GithubFeed):
    def __init__(self, *args):
        GithubFeed.__init__(self, *args)
        self.url = "%(base)s/pulls" % { "base": self.base }

    def __call__(self, params):
        url = "%(orig)s/%(repo)s" % { "orig": self.url, "repo": params.pop("repo") }

        rep = requests.get(url, params)
        return json.loads(resp.text)
