# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 19:30:37 2022

@author: jerry
"""
from math import e, pi, log2

def append_zero(coeffients:list):
    length = len(coeffients)
    if not length&(length-1):
        return
    
    n = 1
    while n < length:
        n <<= 1
    coeffients.extend([0] * (n - length))
    
        

def cooleytucky_FFT(coefficients:list):
    if len(coefficients) == 1:
        return coefficients
    # 如果系数长度为1，则为常数项，直接返回
    append_zero(coefficients)
    # 把系数扩展为2的幂次个
    length = len(coefficients)
    # 扩展后系数个数
    
    result = [0] * length
    # 初始化输出序列
    for i in range(1, round(log2(length))):
        w0 = e ** (2 * pi * 1j / 2 ** (i + 1))
        w = 1
        
        n = length // 2 ** i
        for j in range(length // n):
            for k in range(n):
                coefficients[j * n + k]
        w *= w0
    
    w0 = e ** (2 * pi * 1j / length)
    # 单位根
    w = 1
    # 初始
    
    a0 = [x for i, x in enumerate(coeffients) if i%2 == 0]
    a1 = [x for i, x in enumerate(coeffients) if i%2 != 0]
    # 系数按奇偶分类
    
    y0 = recursive_FFT(a0)
    y1 = recursive_FFT(a1)
    # 迭代过程
    
    for x in range(length // 2):
        result[x] = y0[x] + w * y1[x]
        result[x + length//2] = y0[x] - w * y1[x]
        # yk = y0[k] + x * y1[k]
        w = w0 * w
    return result


    # >>> fft([1, 2, 3, 4])
    # [10, -2 - 2*I, -2, -2 + 2*I]

f = [1,2,3,4]
# fx = 1 + 2x^2 + 3x^3 + 4x^4
print(cooleytucky_FFT(f))


