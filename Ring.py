# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 12:18:48 2022

@author: jerry
"""

import numpy as np

class Ring:
    def __init__(self, q=864, d=4, x=[1]*16):
        # polynomial ring
        # param Rq = Z[x]/(x^(2^d)+1)
        self.modulo = q
        self.d = d
        self.dimension = 2 ** d
        self.mod_poly = np.array([-1] + [0] * self.dimension)
        # if len(x) < 2 ** d:
        #     print("Warning: dimension too small", x)
        self.poly = np.array(x)
        self._balance()
        
    def _balance(self):
        while self.poly.size > self.dimension:
           quotient, remainder = np.polydiv(self.poly, self.mod_poly)
           # print(quotient, remainder)
           self.poly = np.polyadd(remainder , quotient)
        self._coefficient_mod_q()
        
    def _verify(self, other):
        if self.dimension != other.dimension or self.modulo != other.modulo:
            raise RuntimeError("Ring param error!")
    
    def _coefficient_mod_q(self):
        # pass
        self.poly = self.poly % self.modulo
        
    def __add__(self, other):
        self._verify(other)
        return Ring(self.modulo, self.d, np.polyadd(self.poly, other.poly))
    
    def __mul__(self, other):
        self._verify(other)
        return Ring(self.modulo, self.d, np.polymul(self.poly, other.poly))
    
    def __str__(self):
        return str(np.poly1d(self.poly))
    
    def __repr__(self):
        return str(self.poly)