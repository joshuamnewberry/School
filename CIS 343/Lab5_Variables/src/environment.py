from ast import Dict
from typing import Any

class Environment:
    def __init__(self, parent):
        self.dict = {}
        self.parent = parent

    def define (self, name:str, value:Any):
        self.dict.update({name:value})

    def get (self, name):
        if name in self.dict.keys():
            return self.dict.get(name)

    def assign (self, name, value):
        pass