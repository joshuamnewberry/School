from __future__ import annotations
from typing import Any
from environment import Environment
from noggin_token import Token
from error_handler import NogginRuntimeError
from token_type import TokenType
from stmt import *
from expr import *

class NogginCallable:
    def arity(self) -> int:
        raise NotImplementedError

    def call(self, interpreter, arguments):
        raise NotImplementedError

class NogginFunction(NogginCallable):
    def __init__(self, declaration: Function, closure, is_initializer=False):
        self.declaration = declaration
        self.closure = closure
        self.is_initializer = is_initializer
        self.bound_instance = None

    def bind(self, instance):
        this_token = Token(TokenType.THIS, "this", None, 0)
        env = Environment(self.closure)
        env.define(this_token, instance)
        bound = NogginFunction(self.declaration, env, self.is_initializer)
        bound.bound_instance = instance  # store instance for use in call
        return bound

    def arity(self):
        return len(self.declaration.parameters)

    def call(self, interpreter, arguments):
        local_env = Environment(self.closure)

        if self.bound_instance is not None:
            this_token = Token(TokenType.THIS, "this", None, 0)
            local_env.define(this_token, self.bound_instance)

        for index, param in enumerate(self.declaration.parameters):
            local_env.define(param, arguments[index])
        try:
            interpreter.execute_block(self.declaration.block.statements, local_env)
        except NogginReturn as r:
            if self.is_initializer:
                if r.value is not None:
                    raise NogginRuntimeError(self.declaration.name, "Cannot return a value from an initializer")
                return self.closure.get_at(0, Token(TokenType.THIS, "this", None, 0))
            return r.value

        if self.is_initializer:
            return self.closure.get_at(0, Token(TokenType.THIS, "this", None, 0))
        return None

class NogginReturn(Exception):
    def __init__(self, value):
        self.value = value

class NogginClass(NogginCallable):
    def __init__(self, name: str, methods: dict[str, NogginFunction]):
        self.name = name
        self.methods = methods

    def find_method(self, name: str):
        return self.methods.get(name)

    def arity(self):
        initializer = self.find_method("init")
        if initializer:
            return initializer.arity()
        return 0

    def call(self, interpreter, arguments):
        instance = NogginInstance(self)
        initializer = self.find_method("init")
        if initializer:
            initializer.bind(instance).call(interpreter, arguments)
        return instance

    def __str__(self):
        return f"<class {self.name}>"

class NogginInstance:
    def __init__(self, klass: NogginClass):
        self.klass = klass
        self.fields = {}

    def get(self, name: Token):
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]

        method = self.klass.find_method(name.lexeme)
        if method:
            return method.bind(self)

        raise NogginRuntimeError(name, f"Undefined property {name.lexeme}")

    def set(self, name: Token, value: Any):
        self.fields[name.lexeme] = value
        return value

    def __str__(self):
        return f"<instance {self.klass.name}>"