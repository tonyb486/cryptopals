#!/usr/bin/env python3

from binascii import hexlify, unhexlify
from base64 import b64encode, b64decode


def xor(a, b):
    if len(a)!=len(b):
       raise Exception("Invalid Length")
    
    return bytes([a[i]^b[i] for i in range(len(a))])


a = unhexlify("1c0111001f010100061a024b53535009181c")
b = unhexlify("686974207468652062756c6c277320657965")
c = xor(a,b)

assert hexlify(c) == b"746865206b696420646f6e277420706c6179"

print(c.decode("utf-8"))



