# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 04:46:49 2022

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
        pass
        # self.poly = self.poly % self.modulo
        
    def __add__(self, other):
        self._verify(other)
        return Ring(self.modulo, self.d, np.polyadd(self.poly, other.poly))
    
    def __mul__(self, other):
        self._verify(other)
        return Ring(self.modulo, self.d, np.polymul(self.poly, other.poly))
    
    def __str__(self):
        return str(np.poly1d(self.poly))
        
# class Scheme:
#     def __init__(self, q, d,)
if __name__ == "__main__":
    val = 0
    while True:
        a = Ring(d=4,x=np.random.randint(0,11,16))
        b = Ring(d=4,x=np.random.randint(0,3,16))
        c = a * b
        # print(a,b,c)
        arr = c.poly
        temp = np.linalg.norm(c.poly,2)/np.linalg.norm(a.poly,2)/np.linalg.norm(b.poly,2)
        
        if temp > val:
            val = temp 
            print(val)
    
    
    # c = Ring(d=2,x=[10,2,3,4,5,6,7,8,2,2,2,2,2])
    # print(c)
    # d = Ring(d=2,x=[1365,752,447,663,528,499,7777])
    # print(d)
    # f = c * d
    # print(f)