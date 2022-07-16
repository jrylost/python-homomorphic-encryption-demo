# -*- coding: utf-8 -*-
"""
Created on Sat Jul 16 19:38:56 2022

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

def TwoDimension_FFT(coefficients:list, rows:int, columns:int):
    assert len(coefficients) == rows * columns
    
    c = [[coefficients[columns*i + x] for i in range(rows)] for x in range(columns)]
    # 排布系数矩阵
    c = [recursive_FFT(x) for x in c]
    # 按列作FFT
    w = e ** (2 * pi * 1j / rows / columns)
    c = [[i * w ** (index * index2) for index2, i in enumerate(x)] for index, x in enumerate(c)]
    # 乘以twiddle factors
    
    c = [[i[x] for i in c] for x in range(rows)]
    # 转置矩阵
    c = [recursive_FFT(x) for x in c]
    # 按行作FFT
    c = [c[y][x] for x in range(columns) for y in range(rows)]
    # 按列顺序输出结果
    return c

f = [x for x in range(1,17)]
print(TwoDimension_FFT(f,4,4))

# 正确结果
# [136, -8.0 - 40.218715937*I, -8.0 - 19.313708499*I, -8.00000000001 - 11.9728461013*I, -8.0 - 8.0*I, -8.0 - 5.34542910335*I, -8.0 - 3.31370849898*I, -8.0 - 1.59129893904*I, -8, -8.0 + 1.59129893903*I, -8.0 + 3.31370849898*I, -8.0 + 5.34542910336*I, -8.0 + 8.0*I, -8.0 + 11.9728461013*I, -8.0 + 19.313708499*I, -8.0 + 40.218715937*I]