# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 12:18:48 2022

@author: jerry
"""

import numpy as np
import math

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
        self.poly = np.array(x, dtype=np.int64) if type(x) != int else np.array([x]) 
        # self.poly = np.array(x)
        self._balance()
        
    def _balance(self):
        length = len(self.poly)
        if length % self.dimension:
            self.poly = np.append( [0] * (self.dimension - length % self.dimension), self.poly)
            length = (length + self.dimension - 1) // self.dimension * self.dimension
        self.poly = self.poly[::-1]
        for i in range(1, (length + self.dimension-1) // self.dimension):
            self.poly[0:self.dimension] += (-1 ** i) * self.poly[i*self.dimension: (i+1) * self.dimension]
        self.poly = self.poly[0:self.dimension]
        self.poly = self.poly[::-1]
        
        # while self.poly.size > self.dimension:
        #     quotient, remainder = np.polydiv(self.poly, self.mod_poly)
        #     # print(quotient, remainder)
        #     self.poly = np.polyadd(remainder, quotient)
        # 调用numpy接口的balance代码，deprecated
        # self._coefficient_mod_q()
        
    def _verify(self, other):
        if self.dimension != other.dimension or self.modulo != other.modulo:
            # print(self.dimension, other.dimension, self.modulo, other.modulo)
            raise RuntimeError("Ring param error!")
    
    def _coefficient_mod_q(self):
        # pass
        def mod(n):
            temp = n % self.modulo
            if temp > abs(temp - self.modulo):
                return temp - self.modulo
            else:
                return temp
        mod = np.vectorize(mod)
        self.poly = mod(self.poly)
        
    def __add__(self, other):
        self._verify(other)
        r = Ring(self.modulo, self.d, np.polyadd(self.poly, other.poly))
        r._coefficient_mod_q()
        return r
    
    def coefficient_add(self, other):
        self._verify(other)
        r = Ring(self.modulo, self.d, np.polyadd(self.poly, other.poly))
        return r
    
    def __mul__(self, other):
        self._verify(other)
        r = Ring(self.modulo, self.d, np.polymul(self.poly, other.poly))
        r._coefficient_mod_q()
        return r
    
    def __matmul__(self, other):
        self._verify(other)
        return Ring(self.modulo, self.d, np.polymul(self.poly, other.poly))
    
    def __str__(self):
        return str(np.poly1d(self.poly))
    
    def __repr__(self):
        return str(self.poly)
    
    def div_and_round(self, t, q):
        r = Ring(self.modulo, self.d, np.round(self.poly * t / q))
        r._balance()
        r._coefficient_mod_q()
        return r
    
    # def extend(self, base):
    #     l = 0
    #     q = self.modulo
    #     while q >= base:
    #         q = q // base
    #         l += 1
            
    #     for i in range(l+1):

    def decompose(self, base):
        l = np.floor(math.log(self.modulo, base))
        r = []
        poly = self.poly.copy()
        sign = poly // abs(poly)
        poly = abs(poly)
        while l >= 0:
            r.append(Ring(self.modulo, self.d, (poly % base) * sign))
            poly = poly // base
            l -= 1
        return r

if __name__ == "__main__":
    r = Ring(q=864, d=4, x=[i*80 for i in range(16)])
    print(r.__repr__())
    r = r.decompose(7)
    print(r)
    
    
    