# -*- coding: utf-8 -*-
"""
Created on Sat Feb  5 13:31:41 2022

@author: jerry
"""
import numpy as np

class Ring:
    '''
    定义环
    设置环上运算函数
    '''
    def __init__(self, q, d, x):
        # polynomial ring
        # param Rq = Z[x]/(x^(2^d)+1)
        self.modulo = q
        self.d = d
        self.dimension = 2 ** d
        self.mod_poly = np.array([-1] + [0] * self.dimension)
        # if len(x) < 2 ** d:
        #     print("Warning: dimension too small", x)
        self.poly = np.array(x, dtype=np.int64)
        # self.poly = np.array(x)
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
    
    
q=1874
# 多项式系数的模
d=4
n = 2 ** d
# 多项式次数n为2的d次幂
t=7
# 原文的模
B=2
# 设定error的上限
assert q // t > 2 * B * (2 * n + 1)
# 需要满足上述要求才能保证加密的正确性
delta = Ring(q, d, q // t)
# 论文中的delta值


def const_value(x):
    return Ring(q, d, [x])

def generate_secret():
    return Ring(q, d, np.random.randint(0, 2, n))

def generate_a():
    return Ring(q, d, np.random.randint(0, q, n))

def generate_error():
    # return Ring(q, d, [B] * n)
    return Ring(q, d, np.random.randint(0, B+1, n))

def encrypt(m):
    m = Ring(q, d, m)
    u = Ring(q, d, np.random.randint(0, 2, n))
    # u = Ring(q, d, [1]*n)
    ct0 = pk0 * u + generate_error() + delta * m
    ct1 = pk1 * u + generate_error()
    return ct0, ct1

def decrypt(ct0, ct1):
    plain = ct0 + ct1 * s
    plain_vector = np.round(plain.poly * t / q) % t
    return plain_vector

s = generate_secret()
a = generate_a()
pk0 = const_value(-1) * a * s + generate_error()
pk1 = a

m = np.random.randint(0,7,16)
print("原文  ：",np.array(m,dtype=np.float64))

ct0, ct1 = encrypt(m)
print("解密后：",decrypt(ct0, ct1))
