#!/usr/bin/env python3

import math
from binascii import hexlify, unhexlify
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Random import random
from Crypto import Random
from c09 import pad_pkcs7
from c06 import to_blocks

def encryption_oracle(data):
    rndfile = Random.new()
    mode = random.choice([AES.MODE_ECB, AES.MODE_CBC])
    if mode == AES.MODE_ECB:
        print("Using ECB!")
        crypt = AES.new(rndfile.read(16), mode)
    else: 
        print("Using CBC!")
        crypt = AES.new(rndfile.read(16), mode, rndfile.read(16))
        
    plaintext = rndfile.read(random.randrange(5,10)) + data + rndfile.read(random.randrange(5,10)) 
    return crypt.encrypt(pad_pkcs7(plaintext, 16))
    
def detect_mode(enc_function):
    sample = enc_function(b"A"*256)
    blocks = to_blocks(sample, 16)
    # We should've made at least 14 identical blocks of all "A"'s
    if len(blocks) - len(set(blocks)) >= 14:
        return AES.MODE_ECB
    else:
        return AES.MODE_CBC

if __name__ == "__main__":
    for i in range(10):
        mode = detect_mode(encryption_oracle)
        if mode == AES.MODE_ECB: print("Detected ECB!")
        if mode == AES.MODE_CBC: print("Detected CBC!") # (Well, not-ECB!)
