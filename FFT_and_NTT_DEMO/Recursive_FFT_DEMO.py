# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 19:30:37 2022

@author: jerry
"""
from math import e, pi, cos , sin

def append_zero(coefficients:list):
    length = len(coefficients)
    if not length&(length-1):
        return
    
    n = 1
    while n < length:
        n <<= 1
    coefficients.extend([0] * (n - length))
    
        

def recursive_FFT(coefficients:list):
    if len(coefficients) == 1:
        return coefficients
    # 如果系数长度为1，则为常数项，直接返回
    append_zero(coefficients)
    # 把系数扩展为2的幂次个
    length = len(coefficients)
    # 扩展后系数个数
    
    result = [0] * length
    # 初始化输出序列
    
    w0 = e ** (2 * pi * 1j / length)
    
    ang = 2 * pi / length
    w0 = cos(ang) + 1j * sin(ang) 
    # 单位根
    w = 1
    # 初始
    
    a0 = [x for i, x in enumerate(coefficients) if i%2 == 0]
    a1 = [x for i, x in enumerate(coefficients) if i%2 != 0]
    # 系数按奇偶分类
    
    y0 = recursive_FFT(a0)
    y1 = recursive_FFT(a1)
    # 迭代过程
    
    for x in range(length // 2):
        result[x] = y0[x] + w * y1[x]
        result[x + length//2] = y0[x] - w * y1[x]
        # yk = y0[k] + x * y1[k]
        w = w0 ** (x + 1)
        # print(x, w/w0)
    return result






















