#!/usr/bin/env python3

import code, json

from binascii import hexlify, unhexlify
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto import Random

from c03 import break_single_xor
from c05 import xorstr
from c06 import to_blocks
from c18 import aes_ctr

rndfile = Random.new()
key = rndfile.read(16)

# Here is the challenge
plaintexts  = [b64decode(i) for i in open("c19_data.txt").readlines()]
ciphertexts = [aes_ctr(key, 1234, i) for i in plaintexts]
plaintexts = [b'' for i in ciphertexts]

max_len = max([len(i) for i in ciphertexts])
print(plaintexts)

# Let's try frequency analysis on the each byte of each of them
#
# (Okay, this turns out to be the same as transposing it and solving it
#  as a repeating xor key as in challenge 20)
#

key = b''
for n in range(max_len):
    n_bytes = bytes([i[n] for i in ciphertexts if n<len(i)])
    key += bytes([break_single_xor(n_bytes)])

for i in ciphertexts:
    print(xorstr(i, key))
            
# Drop to a console to play with it some more
# The approach above gets most of the keystream, up to
# about 30 bytes it looks correct.

code.InteractiveConsole(locals=globals()).interact()

