import unittest

import github_cli.config as c
import os
import yaml
import tempfile
import shutil

class TestConfig(unittest.TestCase):

    def setUp(self):
        self.conf = c.Config()
        os.environ["HOME"] = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(os.environ["HOME"])

    def test_respects_GHCLI_CONFIG(self):
        # TODO Wrap environment to automate cleanup
        os.environ["GHCLI_CONFIG"] = "/tmp/__hardcoded__"
        self.assertEqual(self.conf.config_path(), "/tmp/__hardcoded__")

    def test_catches_empty_config(self):
        with self.assertRaises(c.NonexistantGHConfigError):
            self.conf['name']

    def test_catches_incomplete_config(self):
        with self.assertRaises(c.InvalidGHConfigError):
            with open(self.conf.config_path(), 'w') as f:
                f.write(yaml.dump({ "name": "richo" }))
            self.conf["name"]

if __name__ == '__main__':
    unittest.main()
