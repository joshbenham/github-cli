import json
import requests
import github_cli.config
from github_cli.github import Github

class Issues:

    allowed_filters = ['assigned', 'created', 'mentioned', 'subscribed']
    allowed_states = ['open', 'closed']
    allowed_sort = ['created', 'updated', 'comments']
    allowed_directions = ['asc', 'desc']

    def __init__(self, args):
        self.args = args

    def execute(self):
        params = {}

        if self.args.user:
            params['user'] = self.args.user[0]
        
        if self.args.repo:
            params['repo'] = self.args.repo[0]

        if self.args.labels:
            params['labels'] = self.args.labels[0]

        if self.args.filter[0] in self.allowed_filters:
            params['filter'] = self.args.filter[0]

        if self.args.state[0] in self.allowed_states:
            params['state'] = self.args.state[0]

        if self.args.sort[0] in self.allowed_sort:
            params['sort'] = self.args.sort[0]

        if self.args.direction[0] in self.allowed_directions:
            params['direction'] = self.args.direction[0]

        gh = Github("https://api.github.com")
        ret = gh.issues(params)

        for issue in ret:
            print('[ %(url)s ] %(title)s' % { 'url': issue['html_url'], 'title': issue['title']})

