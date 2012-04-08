import os
import shutil
import tempfile

MESSAGE_TEMPLATE = """\
Enter your pull request template here

The first line will become the title, the remainder will become the body. The
seperating newline will be removed.
"""

class NoMessageError(Exception): pass
class NoTitleError(Exception): pass

class MessageParser:

    def __init__(self):
        self.data = False

    def mtime(self):
        return os.stat(self.file).st_mtime

    def editor_session(self):
        try:
            self.dir = tempfile.mkdtemp()
            # Name it like a git commit, we'll inherit the same hilights
            self.file = os.path.join(self.dir, "COMMIT_EDITMSG")
            with open(self.file, 'w') as fh:
                fh.write(MESSAGE_TEMPLATE)

            mtime = self.mtime()

            os.system("%s %s" % (os.environ["EDITOR"], self.file))

            if self.mtime() != mtime:
                with open(self.file, 'r') as fh:
                    self.data = fh.readlines()

        finally:
            shutil.rmtree(self.dir)

    def parse_data(self):
        # TODO Refactor this, it's guaranteed to be called twice
        message = ""
        title = self.data[0]
        offset = 1

        try:
            # The short version is that no message is theoretically valid.
            # Probably stupid, but valid.
            if self.data[1] == os.linesep:
                offset += 1

            message = self.data[offset:]
        except:
            pass
        return [title.rstrip(), ''.join(message)]

    def get_message(self):
        if not self.data:
            self.editor_session()
        if not self.data:
            raise NoMessageError
        n =  self.parse_data()[1]
        print(n)
        return n

    def get_title(self):
        if not self.data:
            self.editor_session()
        if not self.data:
            raise NoTitleError
        n = self.parse_data()[0]
        print(n)
        return n

