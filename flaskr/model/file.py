from importlib.resources import path
from select import select
from unicodedata import name


class File:

    def __init__(self, id, name, path, ext, host):
        self.id = id
        self.name = name
        self.path = path
        self.ext = ext
        self.host = host

    def addFile(self):
        return {
            'name': self.name,
            'path': self.path,
            'ext': self.ext,
        }

    def getFile(self):
        return {
            'name': self.name,
            'path': self.path,
            'ext': self.ext,
            'host': self.host
        }
