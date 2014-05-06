# -*- coding: utf-8 -*-

from types import Environment, LispError, Closure
from ast import is_boolean, is_atom, is_symbol, is_list, is_closure, is_integer
from asserts import assert_exp_length, assert_valid_definition, assert_boolean
from parser import unparse

"""
This is the Evaluator module. The `evaluate` function below is the heart
of your language, and the focus for most of parts 2 through 6.

A score of useful functions is provided for you, as per the above imports, 
making your work a bit easier. (We're supposed to get through this thing 
in a day, after all.)
"""

def _eval_quote(ast, env): 
    return evaluate(ast[0], env)

def _eval_atom(ast, env):
    return is_atom(evaluate(ast[0], env))

def _eval_eq(ast, env):
    ast = evaluate(ast, env)
    if not is_atom(ast[0]) or not is_atom(ast[1]): 
        return False 
    return ast[0] == ast[1]

def _add(a1, a2): 
    return a1 + a2

def _sub(a1, a2): 
    return a1 - a2

def _multiply(a1, a2): 
    return a1 * a2

def _divide(a1, a2): 
    return a1 / a2

def _mod(a1, a2): 
    return a1 % a2

def _is_greater(a1, a2): 
    return a1 > a2

def _eval_control(ast, env): 
    if evaluate(ast[0], env): 
        return evaluate(ast[1], env)
    return evaluate(ast[2], env)

def _define_var(ast, env): 
    if len(ast) != 2: 
        raise LispError("Wrong number of arguments")

    if not is_symbol(ast[0]): 
        raise LispError("non-symbol")

    env.set(ast[0], evaluate(ast[1], env))
    return []

def _define_closure(ast, env): 
    if len(ast) != 2: 
        raise LispError("Wrong number of arguments")

    if not is_list(ast[0]): 
        raise LispError("Params of lambda must be a list")
    return Closure(env, ast[0], ast[1])

def _cons(ast, env): 
    item, _list = evaluate(ast[0], env), evaluate(ast[1], env)
    _list.insert(0, item)
    return _list

def _head(ast, env): 
    _list = evaluate(ast[0], env)
    try: 
        return _list[0]
    except IndexError:
        raise LispError('List index out of range') 

def _tail(ast, env): 
    _list = evaluate(ast[0], env)
    try: 
        return _list[1:]
    except IndexError:
        raise LispError('List index out of range') 

def _empty(ast, env): 
    _list = evaluate(ast[0], env)
    if len(_list):
        return False
    return True

EVAL_EXP = {
    'quote': _eval_quote, 
    'atom': _eval_atom, 
    'eq': _eval_eq, 
}

MATH_EXP = {
    '+': _add, 
    '-': _sub,
    '*': _multiply, 
    '/': _divide, 
    'mod': _mod, 
    '>': _is_greater, 
}

CONTROL_EXP = {
    'if': _eval_control
}

VAR_EXP = {
    'define': _define_var, 
}

CLOSURE_EXP = {
    'lambda': _define_closure, 
}

LIST_EXP = {
    'cons': _cons, 
    'head': _head, 
    'tail': _tail, 
    'empty': _empty,
}

def evaluate(ast, env):
    """Evaluate an Abstract Syntax Tree in the specified environment.
    """
    print ast
    if is_atom(ast) or ast == []: 
        if is_symbol(ast):
            return evaluate(env.lookup(ast), env)
        else: 
            return ast 

    if is_list(ast[0]): 
        ast[0] = evaluate(ast[0], env)

    if ast[0] in MATH_EXP.keys():
        return _evaluate_math(ast, env)

    for _map in (CONTROL_EXP, EVAL_EXP, VAR_EXP, CLOSURE_EXP, LIST_EXP): 
        if ast[0] in _map.keys(): 
            func = _map[ast[0]]
            return evaluate(func(ast[1:], env), env)

    if is_symbol(ast[0]): 
        ast[0] = env.lookup(ast[0])

    if is_closure(ast[0]):
        if len(ast[1:]) != len(ast[0].params): 
            raise LispError('wrong number of arguments, expected %s got %s' % (len(ast[0].params), len(ast[1:])))
        arguments = [evaluate(arg, env) for arg in ast[1:]] 
        parameters = dict(zip(ast[0].params, arguments))
        env = ast[0].env.extend(parameters)
        return evaluate(ast[0].body, env)

    return [evaluate(a, env) for a in ast]

def _evaluate_math(ast, env): 
    func = MATH_EXP[ast[0]]
    a1, a2 = evaluate(ast[1], env), evaluate(ast[2], env)
    if not is_integer(a1) or not is_integer(a2): 
        raise LispError('You can only do math on numbers')
    return func(a1, a2) 
