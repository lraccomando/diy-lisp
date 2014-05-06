# -*- coding: utf-8 -*-

"""
This module holds some types we'll have use for along the way.

It's your job to implement the Closure and Environment types.
The LispError class you can have for free :)
"""

class LispError(Exception): 
    """General lisp error class."""
    pass

class Closure:
    
    def __init__(self, env, params, body):
        self.env = env
        self.params = params 
        self.body = body

    def __str__(self):
        return "<closure/%d>" % len(self.params)

class Environment:

    def __init__(self, variables=None):
        self.variables = variables if variables else {}

    def lookup(self, symbol):
        try: 
            return self.variables[symbol]
        except KeyError:
            raise LispError(symbol)

    def extend(self, variables):
        new_vars = dict(self.variables.items() + variables.items())
        return Environment(new_vars)

    def set(self, symbol, value):
        if symbol in self.variables: 
            raise LispError("already defined")
        self.variables[symbol] = value