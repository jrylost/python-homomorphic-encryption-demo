# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 04:46:49 2022

@author: jerry
"""

from Scheme import Scheme
        
if __name__ == "__main__":
    scheme = Scheme()
    ct0, ct1 = scheme.encrypt([1,2,3,6,1,5,3,4])
    plain = scheme.decrypt(ct0, ct1)
    print(plain)
    
    