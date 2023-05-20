import os


class Common():
    def getHome(self):
        return os.path.expanduser('~')
