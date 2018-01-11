#!/usr/bin/env python3

import math
from binascii import hexlify, unhexlify
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from c06 import to_blocks
from c05 import xorstr

def unpad(data):
    plen = data[-1]
    if data[-plen:] != bytes([plen]*plen):
        raise Exception("Invalid Padding (got '%s', expected %d bytes)!" % (data[-plen:], plen))
    else:
        return data[:-plen]

# Success        
assert unpad(b"ICE ICE BABY\x04\x04\x04\x04") == b"ICE ICE BABY"

# Failure (which is, of course, success)
try:
    unpad(b"ICE ICE BABY\x05\x05\x05\x05") 
    print("Error!")
except: pass

try:
    unpad(b"ICE ICE BABY\x01\x02\x03\x04") 
    print("Error!")
except: pass


