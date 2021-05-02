# -*- coding: utf-8 -*-
import math
import re
import sys
import operator
from functools import reduce


class Operator:

    P_CST = 6 #定数
    P_LHB = 5 #!
    P_FUN = 4 #関数
    P_POW = 3 #累乗
    P_UPM = 2 #単項の+,-
    P_MD = 1 #*,/,%
    P_BPM = 0 #2項の+,-

    def __init__(self, name, fun, priority):

        self.name = name
        self.fun = fun
        self.priority = priority

    def __call__(self, x = None, y = None):

        return self.fun if self.is_const() else \
            self.fun(x) if self.is_unary() or self.is_lhb() else \
                self.fun(x,y)

    def __gt__(self, other):

        assert other is None or isinstance(other, Operator)
        return other is None or \
            self.priority > other.priority or \
                (self.priority in (Operator.P_FUN, Operator.P_POW, Operator.P_UPM) and self.priority == other.priority)

    def __str__(self):

        return self.name

    def __repr__(self):

        return repr(self.name)

    def  is_const(self):

        return self.priority == Operator.P_CST

    def is_lhb(self):

        return self.priority == Operator.P_LHB
    
    def is_upm(self):

        return self.priority == Operator.P_UPM

    def is_func(self):

        return self.priority == Operator.P_FUN

    def is_unary(self):

        return self.priority in (Operator.P_FUN, Operator.P_UPM)

    def is_binary(self):

        return self.priority in (Operator.P_POW, Operator.P_MD, Operator.P_BPM)

    
def is_natural(n):

    return type(n) is int and n >= 0

def fact(n):

    assert is_natural(n)
    return reduce(operator.__mul__, range(1, n+1)) if n > 0 else 1

def permutation(m, n):

    assert is_natural(m) and is_natural(n) and m >= n
    return reduce(operator.__mul__, range(m - n+1, m+1), 1)

def combination(m, n):

    assert is_natural(m) and is_natural(n) and m >= n
    return permutation(m, n)/fact(n)


L_OP = [\
    Operator('@+', operator.__pos__, Operator.P_UPM), \
        Operator('@-', operator.__neg__, Operator.P_UPM), \
            Operator('+', operator.__add__, Operator.P_BPM), \
                Operator('-', operator.__sub__, Operator.P_BPM), \
                    Operator('*', operator.__mul__, Operator.P_MD), \
                        Operator('/', operator.__truediv__, Operator.P_MD), \
                            Operator('%', operator.__mod__, Operator.P_MD), \
                                Operator('<<', operator.__lshift__, Operator.P_POW), \
                                    Operator('>>', operator.__rshift__, Operator.P_POW), \
                                        Operator('**', math.pow, Operator.P_POW), \
                                            Operator('^', math.pow, Operator.P_POW), \
                                                Operator('exp', math.exp, Operator.P_FUN), \
                                                    Operator('log', math.log, Operator.P_FUN), \
                                                        Operator('log10', math.log10, Operator.P_FUN), \
                                                            Operator('sqrt', math.sqrt, Operator.P_FUN), \
                                                                Operator('abs', operator.__abs__, Operator.P_FUN), \
                                                                    Operator('sin', math.sin, Operator.P_FUN), \
                                                                        Operator('cos', math.cos, Operator.P_FUN), \
                                                                            Operator('tan', math.tan, Operator.P_FUN), \
                                                                                Operator('asin', math.asin, Operator.P_FUN), \
                                                                                    Operator('acos', math.acos, Operator.P_FUN), \
                                                                                        Operator('atan', math.atan, Operator.P_FUN), \
                                                                                            Operator('!', fact, Operator.P_LHB), \
                                                                                                Operator('P', permutation, Operator.P_POW), \
                                                                                                    Operator('C', combination, Operator.P_POW), \
                                                                                                        Operator('pi', math.pi, Operator.P_CST), \
                                                                                                            Operator('e', math.e, Operator.P_CST), \
    ]


H_OP = dict([(str(op), op) for op in L_OP])


def convert_op_name(op):
    return ''.join([(c if c.isalnum() else '\\' + c) for c in str(op)]) + \
        (r'(?=\W|$)' if op.is_const() else r'(?=[\s\(])' if op.is_func else'')


RE_FORM =re.compile(\
    r'''(?P<nest>\() |
        (?P<num>\d+(?P<after_dot>\.\d+)?(?:[eE][+-]?\d+)?) |
        (?P<op_name>%%s)
    '''%('|'.join([ convert_op_name(op) for op in sorted([op for op in L_OP if not op.is_upm()], key=lambda x:len(str(x)), reverse=True)]),),\
        re.VERBOSE)


def cons(obj, ls):

    ls.append(obj)
    return ls


def operator_position(ls):

    tprev, term0, pos = None, None, -1
    for i, term in enumerate(ls):
        if isinstance(term, Operator) and (term > term0 or (isinstance(tprev, Operator) and term.is_upm())):
            term0, pos = term, i
        tprev = term
    return term0, pos


