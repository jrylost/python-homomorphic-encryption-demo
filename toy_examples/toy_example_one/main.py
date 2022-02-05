# -*- coding: utf-8 -*-
"""
Created on Sat Feb  5 12:38:39 2022

@author: jerry
"""

import numpy as np
from pprint import pprint
#%%
print("*******************加解密过程**********************\n")
s = np.random.randint(0, 1000)
print(f"我们取随机密钥s: {s}\n")

a = np.random.randint(0, 1000)
print(f"我们取随机数a: {a}\n")

pk = (- a * s, a)
print(f"计算得出pk: {pk}, pk_0: {pk[0]}, pk_1: {pk[1]}\n")

m = np.random.randint(0, 1000)
print(f"我们取随机消息m: {m}\n")

ct = (pk[0] + m, pk[1])
print(f"计算得出ct: {ct}, ct_0: {ct[0]}, ct_1: {ct[1]}\n")

print("解密过程：计算ct_0 + ct_1 * s\n")
decryption_message = ct[0] + ct[1] * s
print(f"计算得出decryption_message: {decryption_message}\n")

#%%
print("*******************同态加法计算*********************\n")


print("同样地，我们选取一个密钥对两组消息进行加密\n")
s = np.random.randint(0, 1000)
print(f"我们取随机密钥s: {s}\n")

a0 = np.random.randint(0, 1000)
pk0 = (- a0 * s, a0)
print(f"计算得出pk0: {pk0}, pk0_0: {pk0[0]}, pk0_1: {pk0[1]}")

a1 = np.random.randint(0, 1000)
pk1 = (- a1 * s, a1)
print(f"计算得出pk1: {pk1}, pk1_0: {pk1[0]}, pk1_1: {pk1[1]}\n")

m0 = np.random.randint(0, 1000)
m1 = np.random.randint(0, 1000)
print(f"我们取随机消息m0, m1: {m0},{m1}\n")

ct0 = (pk0[0] + m0, pk0[1])
ct1 = (pk1[0] + m1, pk1[1])
print(f"计算得出ct0: {ct0}, ct0_0: {ct0[0]}, ct0_1: {ct0[1]}")
print(f"计算得出ct1: {ct1}, ct1_0: {ct1[0]}, ct1_1: {ct1[1]}\n")

print("密文相加后：")
ct_new = (ct0[0] + ct1[0], ct0[1] + ct1[1])
print(f"计算得出ct_new: {ct_new}, ct_new_0: {ct_new[0]}, ct_new_1: {ct_new[1]}")

print("解密得到：")
message_new = ct_new[0] + ct_new[1] * s
print(f"计算得出decryption_message: {message_new} == {m0} + {m1}\n")


#%%
print("*******************同态乘法计算*********************\n")

print("同样地，我们选取一个密钥对两组消息进行加密\n")
s = np.random.randint(0, 1000)
print(f"我们取随机密钥s: {s}\n")

a_eval = np.random.randint(0, 1000)
eval_key = (- a_eval * s + s**2, a_eval)
print(f"计算得出eval_key: {eval_key}, eval_key_0: {eval_key[0]}, eval_key_1: {eval_key[1]}")

a0 = np.random.randint(0, 1000)
pk0 = (- a0 * s, a0)
print(f"计算得出pk0: {pk0}, pk0_0: {pk0[0]}, pk0_1: {pk0[1]}")

a1 = np.random.randint(0, 1000)
pk1 = (- a1 * s, a1)
print(f"计算得出pk1: {pk1}, pk1_0: {pk1[0]}, pk1_1: {pk1[1]}\n")

m0 = np.random.randint(0, 1000)
m1 = np.random.randint(0, 1000)
print(f"我们取随机消息m0, m1: {m0},{m1}\n")

ct0 = (pk0[0] + m0, pk0[1])
ct1 = (pk1[0] + m1, pk1[1])
print(f"计算得出ct0: {ct0}, ct0_0: {ct0[0]}, ct0_1: {ct0[1]}")
print(f"计算得出ct1: {ct1}, ct1_0: {ct1[0]}, ct1_1: {ct1[1]}\n")

ct_temp_0 = ct0[0] * ct1[0]
ct_temp_1 = ct0[0] * ct1[1] + ct0[1] * ct1[0]
ct_temp_2 = ct0[1] * ct1[1]
print(f"计算得出ct_temp_0: {ct_temp_0}, ct_temp_1: {ct_temp_1}, ct_temp_2: {ct_temp_2}")

print("密文相乘后：")
ct_new = (ct_temp_0 + ct_temp_2 * eval_key[0], ct_temp_1 + ct_temp_2 * eval_key[1])
print(f"计算得出ct_new: {ct_new}, ct_new_0: {ct_new[0]}, ct_new_1: {ct_new[1]}")

print("解密得到：")
message_new = ct_new[0] + ct_new[1] * s
print(f"计算得出decryption_message: {message_new} == {m0} * {m1}\n")
