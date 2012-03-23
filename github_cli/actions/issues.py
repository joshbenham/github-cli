import json
import urllib
import requests
import github_cli.config

class Issues:

    allowed_filters = ['assigned', 'created', 'mentioned', 'subscribed']
    allowed_states = ['created', 'updated', 'comments']
    allowed_directions = ['asc', 'desc']

    def __init__(self, args):
        self.args = args

    def execute(self):
        get = {}
        url = 'https://api.github.com/issues'
        #if self.args.user and self.args.repo:
        #    url = 'https://api.github.com/repos/%s/%s/issues' % ( self.args.user[0], self.args.repo[0] )

        if self.args.filter[0] in self.allowed_filters:
            get['filter'] = self.args.filter[0]

        if self.args.state[0] in self.allowed_states:
            get['state'] = self.args.state[0]

        if self.args.direction[0] in self.allowed_directions:
            get['direction'] = self.args.direction[0]

        if len(get) > 0:
            url = url + '?' + urllib.urlencode(get)
        
        #print(url)
        a = requests.get(url, data=get)
        print(a.url)
        issues = json.loads(requests.get(url))

        for issue in issues:
            print(issue)

