#!/usr/bin/env python3

import math
from binascii import hexlify, unhexlify
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from c06 import to_blocks
from c05 import xorstr


def check_padding(data):
    plen = data[-1]
    return data[-plen:] == bytes([plen]*plen)

def cbc_decrypt(data, key, iv):
    crypt = AES.new(key, AES.MODE_ECB)
    blocks = [iv] + to_blocks(data, len(key))
    
    blocks = [xorstr(crypt.decrypt(blocks[i]), blocks[i-1]) for i in range(1,len(blocks))]
    plaintext = b"".join(blocks)
    assert check_padding(plaintext)
    return plaintext

data = b64decode(open("c10_data.txt").read())
plaintext = cbc_decrypt(data, b"YELLOW SUBMARINE", bytes([0]*16))

print(plaintext.decode("ascii"))

