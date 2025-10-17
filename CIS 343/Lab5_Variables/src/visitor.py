from expr import *
from error_handler import *

class Visitor:
    def visit(self, node):
        method_name = f'visit_{node.__class__.__name__.lower()}'
        if hasattr(self, method_name):
            return getattr(self, method_name)(node)
        raise NotImplementedError