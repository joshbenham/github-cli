import github_cli.config

class Config:
    def __init__(self, args):
        self.args = args

    def execute(self):
        # TODO Blindly assume that we don't mind nuking config
        print("Launched config task")



