# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 12:19:53 2022

@author: jerry
"""

import numpy as np
from Ring import Ring
        
class Scheme:
    def __init__(self, q=874, d=3, t=7, B=5):
        # q modulo q
        # d x^(2^d)+1
        # B error bound
        self.q = q
        self.t = t
        self.d = d
        self.n = 2 ** d
        self.B = B
        self.delta = Ring(self.q, self.d, q // t)
        self.s = self._generate_secret()
        self.a = self._generate_a()
        self.pk0 = self._const_value(-1) * self.a * self.s + self._generate_error()
        self.pk1 = self.a
        
    def _const_value(self, x):
        return Ring(self.q, self.d, [x])
    
    def _generate_secret(self):
        return Ring(self.q, self.d, np.random.randint(0, 2, self.n))
    
    def _generate_a(self):
        return Ring(self.q, self.d, np.random.randint(0, self.q, self.n))
    
    def _generate_error(self):
        return Ring(self.q, self.d, np.random.randint(0, self.B+1, self.n))
    
    def encrypt(self, m):
        self.m = Ring(self.q, self.d, m)
        u = Ring(self.q, self.d, np.random.randint(0, 2, self.n))
        self.ct0 = self.pk0 * u + self._generate_error() + self.delta * self.m
        self.ct1 = self.pk1 * u + self._generate_error()
        return self.ct0, self.ct1
    
    def decrypt(self, ct0, ct1):
        plain = ct0 + ct1 * self.s
        plain_vector = np.round(plain.poly * self.t / self.q) % self.t
        return plain_vector