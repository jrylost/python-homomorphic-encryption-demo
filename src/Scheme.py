# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 12:19:53 2022

@author: jerry
"""

import numpy as np
import math
from Ring import Ring
        
class Params:
    def __init__(self, q, d, t, B):
        # q modulo q
        # d x^(2^d)+1
        # B error sample bound
        self.q = q
        self.d = d
        self.t = t
        self.B = B
        self.n = 2 ** d
        self.delta = Ring(self.q, self.d, q // t)
    

class Scheme:
    def __init__(self, params):
        self.params = params
        # assert q // t > 2 * self.B * (2 * self.n + 1)
        # error bound
        self.s = self._generate_secret()
        self.a = self._generate_a()
        self.pk0 = self._const_value(-1) * self.a * self.s + self._generate_error()
        self.pk1 = self.a
        
    def _const_value(self, x):
        return Ring(self.params.q, self.params.d, [x])
    
    def _generate_secret(self):
        # r = Ring(self.params.q, self.params.d, [0] * self.params.n)
        # r.poly[-1] = 1
        # return r
        # return Ring(self.q, self.d, [1] * self.n)
        return Ring(self.params.q, self.params.d, np.random.randint(-1, 2, self.params.n))
    
    def _generate_a(self):
        return Ring(self.params.q, self.params.d, np.random.randint(0, self.params.q, self.params.n))
    
    def _generate_error(self):
        # return Ring(self.q, self.d, [self.B] * self.n)
        return Ring(self.params.q, self.params.d, np.random.randint(-self.params.B, self.params.B+1, self.params.n))
    
    def get_public_key_pair(self, baseT=2):
        if baseT:
            rk = RelinearizationKey()
            rk.base = baseT
            s2 = self.s * self.s
            for i in range(np.floor(math.log(self.params.q, baseT)).astype(np.int64) + 1):
                a = self._generate_a()
                rk.append((self._const_value(-1) * a * self.s + self._generate_error() + self._const_value(baseT ** i) * s2, a,))
        else:
            rk = RelinearizationKey()
        # rk =
        
        
        
        return PublicKey(self.params, self.pk0, self.pk1, relinearizationKey=rk)
    
    # @staticmethod()
    def decrypt(self, ciphertext):
        # print(s)
        plain = ciphertext.ct0 + ciphertext.ct1 * self.s
        # plain.poly = plain.poly % self.params.q
        # print(plain.poly)
        # print("??:", plain.poly * self.t / self.q)
        plain_vector = np.round(plain.poly * self.params.t / self.params.q) % self.params.t
        # print("here:", plain_vector)
        def mod(n):
            temp = n % self.params.t
            if temp > abs(temp - self.params.t):
                return temp - self.params.t
            else:
                return temp
        mod = np.vectorize(mod)
        plain_vector = mod(plain_vector)
        # print(plain_vector)
        
        return plain_vector
    
    
    #TODO
    # def _noise(self):
    
    # def _noise_bound(self):
    
    
    # def _noise_exceed_upper_bound():
    
    # def add(self, other):
    
    # def negate(self):
        
    # def mul(self, other):
    
    # def _generate_relinearization_key(self):
    def _verify(self, other):
        if self.q != other.q or self.t != other.t or self.d != other.d:
            raise RuntimeError("Scheme params error!")
        
    def __add__(self, other):
        self._verify(other)
        s = Scheme(self.q, self.d, self.t, self.B + other.B + self.t)
        s.ct0 = self.ct0 + other.ct0
        s.ct1 = self.ct1 + other.ct1
        # print(s.ct0.poly)
        # print(self.ct0.poly * 2)
        return s
    
    # TODO
    # def rotate
    # slot related!!!!

class PublicKey:
    def __init__(self, params, pk0, pk1, relinearizationKey=None, rotationKey=None):
        self.params = params
        self.pk0 = pk0
        self.pk1 = pk1
        self.rk = relinearizationKey
    
    def _generate_error(self):
        # return Ring(self.q, self.d, [self.B] * self.n)
        return Ring(self.params.q, self.params.d, np.random.randint(-1, 2, self.params.n))
    
    
    def encrypt(self, plaintext):
        self.plaintext = Ring(self.params.q, self.params.d, plaintext)
        u = self._generate_error()
        ct0 = self.pk0 * u + self._generate_error() + self.params.delta * self.plaintext
        ct1 = self.pk1 * u + self._generate_error()
        ciphertext = Cipher(self.params, ct0, ct1, self.params.B * (2 * self.params.n + 1))
        if self.rk:
            ciphertext.rk = self.rk
        return ciphertext

class RelinearizationKey(list):
    pass

class Cipher:
    def __init__(self, params, ct0, ct1, noise, rk=None):
        self.params = params
        self.ct0 = ct0
        self.ct1 = ct1
        self.rk = rk
        self.noise = noise
        if not self.params.q // self.params.t > 2 * self.noise:
            raise RuntimeError("Noise exceeds upper bound!")
        
    def _verify(self, other):
        if self.params.q != other.params.q or self.params.t != other.params.t or self.params.d != other.params.d:
            raise RuntimeError("Scheme params error!")
        
    def __add__(self, other):
        self._verify(other)
        return Cipher(self.params, self.ct0 + other.ct0, self.ct1 + other.ct1, self.params.B + other.params.B + self.params.t)
        
    def __mul__(self, other):
        if not self.rk:
            raise RuntimeError("No rk!")
        self._verify(other)
        c0 = self.ct0 @ other.ct0
        c1 = (self.ct0 @ other.ct1).coefficient_add(self.ct1 @ other.ct0) 
        c2 = self.ct1 @ other.ct1
        
        c0 = c0.div_and_round(self.params.t, self.params.q)
        c1 = c1.div_and_round(self.params.t, self.params.q)
        c2 = c2.div_and_round(self.params.t, self.params.q)
        
        c2 = c2.decompose(self.rk.base)
        if len(c2) != len(self.rk):
            raise RuntimeError("c2 and rk doesn't match!")
        
        l1 = []
        l2 = []
        for i in range(len(c2)):
            l1.append(self.rk[i][0] * c2[i])
            l2.append(self.rk[i][1] * c2[i])
            
        
        c0_new = c0
        for x in l1:
            c0_new += x
        c1_new = c1
        for x in l2:
            c1_new += x
        
        c0_new._coefficient_mod_q()
        c1_new._coefficient_mod_q()
        
        noise_relinearization = len(self.rk) * self.params.B * self.params.t * self.params.n / 2
        noise = max(self.noise, other.noise)
        noise = noise * self.params.t * self.params.n * (self.params.n + 1.25) + noise_relinearization
        
        return Cipher(self.params, c0_new, c1_new, noise)
    
    
    
    
    
    
    