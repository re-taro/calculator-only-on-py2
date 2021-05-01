# -*- coding: utf-8 -*-
import math
import re
import sys
import operator

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
