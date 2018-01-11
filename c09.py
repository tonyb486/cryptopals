#!/usr/bin/env python3

import math
from binascii import hexlify, unhexlify
from base64 import b64encode, b64decode
from Crypto.Cipher import AES

def pad_pkcs7(string, size):
    l = len(string)
    padding = size - (l%size)

    return string+bytes([padding])*padding

assert pad_pkcs7(b"YELLOW SUBMARINE", 20) == b'YELLOW SUBMARINE\x04\x04\x04\x04'
