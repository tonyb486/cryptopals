#!/usr/bin/env python3

from binascii import hexlify, unhexlify
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto import Random

from c03 import break_single_xor
from c05 import xorstr
from c06 import to_blocks, transpose
from c18 import aes_ctr

rndfile = Random.new()
key = rndfile.read(16)

# Here is the challenge
plaintexts  = [b64decode(i) for i in open("c20_data.txt").readlines()]
ciphertexts = [aes_ctr(key, 1234, i) for i in plaintexts]

min_len = min([len(i) for i in ciphertexts])
blocks = [i[0:min_len] for i in ciphertexts]
transposed = transpose(blocks, min_len)

key = bytes([break_single_xor(i) for i in transposed])

for i in blocks:
    print(xorstr(i, key))



