import os
import yaml


class InvalidGHConfigError(Exception): pass
class NonexistantGHConfigError(Exception): pass
REQUIRED_KEYS = ("username", "access_token")
DEFAULT_OPTIONS = {}
CLIENT_KEY = "1112a0120246109dc7b3"
CLIENT_SECRET = "66478378df4189a22c0fa2d31de6004826fa0d41"

class Config:

    def __init__(self):
        self._config_ready = False
        self._config = None

    def config_path(self):
        if "GHCLI_CONFIG" in os.environ:
            return os.environ["GHCLI_CONFIG"]
        else:
            return os.path.join(os.environ["HOME"], ".ghcli")

    def __getitem__(self, k):
        # Lazy load config- may not exist yet
        if not self._config:
            self.config_read()
        return self._config[k]

    def __setitem__(self, k, v):
        """Writes an item to the internal state.

        Is not implicitly written to disk at exit
        Will throw errors if written before config is initialised"""
        self._config[k] = v

    def read(self):
        """Wraps config read for the usecase where you want to update keys without reading"""
        self.config_read()

    def write(self):
        """Writes config out to disk"""
        self.config_write()

    def new(self):
        """Creates a new config context for when the user isn't previously configured"""
        self._config = DEFAULT_OPTIONS
        return self

    def config_read(self):
        """Private config reader"""
        try:
            with open(self.config_path(), 'r') as f:
                conf = yaml.load(f.read())
                if self.validate(conf):
                    self._config = conf
                else:
                    raise InvalidGHConfigError
        except IOError:
            raise NonexistantGHConfigError

    def config_write(self):
        """Private config writer"""
        with open(self.config_path(), 'w') as f:
            f.write(yaml.dump(self._config))

    @staticmethod
    def validate(c):
        for i in REQUIRED_KEYS:
            if i not in c:
                raise InvalidGHConfigError("Missing key %(name)s" % { "name": i })
        return True
    def __enter__(self):
        """Compliance with the with protocol"""
        return self
    def __exit__(self, typ, valu, tracebac):
        """When used as a with statement, config is written out at exit"""
        if typ is None:
            self.write()
