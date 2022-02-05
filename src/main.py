# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 04:46:49 2022

@author: jerry
"""

from Scheme import Scheme
import numpy as np

def test_benchmark():
    scheme = Scheme()
    ct0, ct1 = scheme.encrypt([1,2,3,6,1,5,3,4])
    plain = scheme.decrypt(ct0, ct1)

def correctness_test():
    # x = 819600
    while True:
        scheme = Scheme(q=1874, t=7 ,d=4, B=2)
        test_plain = np.random.randint(0,7,16)
        # test_plain = [9] * 1024
        ct0, ct1 = scheme.encrypt(test_plain)
        plain = scheme.decrypt(ct0, ct1)
        if not (plain == test_plain).all():
            print(plain)
            # print(test_plain)
            x +=10
            print(x//10)

if __name__ == "__main__":

    scheme = Scheme(q=1874, t=7 ,d=4, B=2)
    message = np.random.randint(0,7,16)
    print(message)
    ct0, ct1 = scheme.encrypt(message)
    plain = scheme.decrypt(ct0, ct1)
    # print(scheme.s * scheme.pk1 + scheme.pk0)
    print(plain)
    
    # correctness_test()
    
    