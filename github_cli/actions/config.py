import oauth2 as oauth
import socket
import webbrowser

import github_cli.config
from github_cli.github import Github

class OauthWrapper:
    def __init__(self):
        self.host = "oauth.psych0.tk"
        self.port = 2000
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((self.host, self.port))
    def get_id(self):
        # 128 == Size of a uuid
        return self._sock.recv(128)
    def get_code(self):
        n = self._sock.recv(20)
        self._sock.close
        return n

class Config:
    def __init__(self, args):
        self.args = args

    def execute(self):
        # TODO Blindly assume that we don't mind nuking config
        gh = Github("https://api.github.com")
        oauth = OauthWrapper()
        with github_cli.config.Config().new() as conf:
            webbrowser.open(gh.oauth.auth_url(id=oauth.get_id()))

            code = oauth.get_code()
            req_data = {
                "client_id": github_cli.config.CLIENT_KEY,
                "client_secret": github_cli.config.CLIENT_SECRET,
                "code": code
                }

            conf["access_token"] = gh.oauth("access_token", req_data)[u'access_token']
            conf["username"] = self.args.username
