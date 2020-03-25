import numpy as np
import os,sys
import random

def swap(arr,i,j):
    arr2 = arr.copy()
    arr2[i] = arr[j]
    arr2[j] = arr[i]
    return arr2

#swaps num elements in code and decode
def swap_mult(num, code, decode):
    idx_list = np.random.choice(num,np.arange(27),replace=False)

    ord = np.arange(num)
    np.random.shuffle(ord)

    new_idx_list = np.take(idx_list,ord)

    code_prop = code.copy()
    decode_prop = decode.copy()
    for i,elem in enumerate(new_idx_list):
        code_prop[idx_list[i]] = code[elem]
        decode_prop[code[elem]] = idx_list[i]

    return (code_prop, decode_prop)

# returns boolean indicating whether c is a character modelled in transition matrix
# (i.e, lowercase letter, new line, or space)
# assumes c is already lowercased
def invalid(c):
    return (c != 32 and c != 10 and (c < 97 or c > 122))

# converts lowercase ascii letters to nums 0 -> 25, and gives space/NL num 26
def conv_ascii(c):
    assert(not invalid(c))
    if c == 32 or c == 10:
        return 26
    else:
        return c - 97

# undoes transformation of conv_ascii
def deconv_ascii(c):
    if c == 26:
        c = 32
    else:
        c += 97
    assert(not invalid(c))
    return np.int(c)

# given the n-gram, gets relevant indexes of Q to update
def get_idx(gram):
    x = 0
    y = 0
    gram = [conv_ascii(c) for c in gram]

    maxpow = len(gram)-2
    x += gram[0] * 27**maxpow
    for i in range(1,len(gram)-1):
        x += gram[i] * 27**(maxpow-i)
        y += gram[i] * 27**(maxpow-i+1)
    y += gram[-1]

    return [x,y]
