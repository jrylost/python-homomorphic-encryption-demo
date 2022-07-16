# -*- coding: utf-8 -*-
"""
Created on Sat Jul 16 19:38:56 2022

@author: jerry
"""
from Recursive_FFT_DEMO import recursive_FFT
from math import e, pi, cos , sin



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