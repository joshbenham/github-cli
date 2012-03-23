import os
import yaml


class InvalidGHConfigError(Exception): pass
class NonexistantGHConfigError(Exception): pass

class Config:

    REQUIRED_KEYS = ("username", "oauth_token", "oauth_secret")

    def __init__(self):
        self._config_ready = False
        self._config = None

    def config_path(self):
        if "GHGLI_CONFIG" in os.environ:
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
        self.read_config()

    def write(self):
        """Writes config out to disk"""
        self.write_config()

    def new(self):
        """Creates a new config context for when the user isn't previously configured"""
        self._config = {}

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
    def validate(self):
        for i in REQUIRED_KEYS:
            if i not in _config:
                raise InvalidGHConfigError, "Missing key %(name)s" % { "name": i }
        return True
