from importlib.resources import path
from select import select
from unicodedata import name


class File:

    def __init__(self, id, name, path, ext):
        self.id = id
        self.name = name
        self.path = path
        self.ext = ext

    def addFile(self):
        return {
            'name': self.name,
            'path': self.path,
            'ext': self.ext,
        }

    def getFile(self):
        return {
            'host': self.id,
            'name': self.name,
            'path': self.path,
            'ext': self.ext,
        }
