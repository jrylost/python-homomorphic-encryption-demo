# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 04:46:49 2022

@author: jerry
"""

from Scheme import Scheme, Params
import numpy as np

def test_benchmark():
    scheme = Scheme()
    ct0, ct1 = scheme.encrypt([1,2,3,6,1,5,3,4])
    plain = scheme.decrypt(ct0, ct1)

# def correctness_test():
#     # x = 819600
#     while True:
#         scheme = Scheme(q=1874, t=7 ,d=4, B=2)
#         test_plain = np.random.randint(0,7,16)
#         # test_plain = [9] * 1024
#         ct0, ct1 = scheme.encrypt(test_plain)
#         plain = scheme.decrypt(ct0, ct1)
#         if not (plain == test_plain).all():
#             print(plain)
#             # print(test_plain)
#             x +=10
#             print(x//10)

if __name__ == "__main__":
    params = Params(q=2777777, t=7 ,d=4, B=1)
    scheme = Scheme(params)
    print("s:",scheme.s.__repr__())
    pk = scheme.get_public_key_pair(600)
    # print(scheme.s)
    message = np.random.randint(-3,4,16)
    print(message)
    ciphertext = pk.encrypt(message)
    
    message2 = np.random.randint(-3,4,16)
    print(message2)
    ciphertext2 = pk.encrypt(message2)
    
    from Ring import Ring
    a = Ring(7,4,message)
    b = Ring(7,4,message2)
    print((a*b).__repr__())
    
    
    ciphertext3 = ciphertext * ciphertext2
    # message = np.random.randint(-2,3,16)
    # print(message)
    # scheme2 = Scheme(q=27775, t=5 ,d=4, B=0)
    # scheme2.pk0 = scheme.pk0
    # scheme2.pk1 = scheme.pk1
    # ct0, ct1 = scheme2.encrypt(message)
    
    
    # resultScheme = scheme
    # plain = resultScheme.decrypt(scheme.s)
    # print(plain.astype(np.int64))

    # resultScheme = scheme + scheme2
    plain = scheme.decrypt(ciphertext3)
    # print(scheme.s)
    print(plain.astype(np.int64))
    
    # correctness_test()
    
    