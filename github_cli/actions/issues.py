import json
import requests
import github_cli.config
from github_cli.github import Github

class Issues:

    allowed_filters = ['assigned', 'created', 'mentioned', 'subscribed']
    allowed_states = ['created', 'updated', 'comments']
    allowed_directions = ['asc', 'desc']

    def __init__(self, args):
        self.args = args

    def execute(self):
        params = {}
        #if self.args.user and self.args.repo:
        #    url = 'https://api.github.com/repos/%s/%s/issues' % ( self.args.user[0], self.args.repo[0] )

        if self.args.filter[0] in self.allowed_filters:
            params['filter'] = self.args.filter[0]

        if self.args.state[0] in self.allowed_states:
            params['state'] = self.args.state[0]

        if self.args.direction[0] in self.allowed_directions:
            params['direction'] = self.args.direction[0]

        params['user'] = "99designs"
        params['repo'] = "contests"

        gh = Github("https://api.github.com")
        ret = gh.issues(params)
        print(ret)

        for issue in ret:
            print(issue)

