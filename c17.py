#!/usr/bin/env python3

import math
from binascii import hexlify, unhexlify
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Random import random
from Crypto import Random

from c05 import xorstr
from c06 import to_blocks
from c09 import pad_pkcs7
from c15 import unpad


#----------------------------------------------
# The "Server" that we're attacking
# gen_token() generates the encrypted token
# check_token() throws an Exception if padding is invalid
#----------------------------------------------

rndfile = Random.new()
key = rndfile.read(16)

data = [b64decode("MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc="),
        b64decode("MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic="),
        b64decode("MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw=="),
        b64decode("MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg=="),
        b64decode("MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl"),
        b64decode("MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA=="),
        b64decode("MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw=="),
        b64decode("MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8="),
        b64decode("MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g="),
        b64decode("MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93")]

def gen_token():
    global key
    iv = rndfile.read(16)
    crypt = AES.new(key, AES.MODE_CBC, iv)
    plaintext = random.choice(data)
    ciphertext = crypt.encrypt(pad_pkcs7(plaintext, 16))
    return iv+ciphertext

def check_token(token):
    global key
    crypt = AES.new(key, AES.MODE_CBC, token[0:16])    
    plaintext = unpad(crypt.decrypt(token[16:])) # oh no, a padding oracle!
    return True

#----------------------------------------------
# The actual padding oracle attack
#----------------------------------------------    

def do_padding(c1, known):
    if len(known)>0:
        padding = bytes([len(known)+1]*(len(known)))
        to_flip = xorstr(known, padding)
        flipped = xorstr(to_flip, c1[0-len(padding):])   
        return bytearray(c1[:-1*len(padding)]+flipped)
    else:
        return bytearray(c1)

def padding_oracle_block(c1, c2, oracle):
    c1 = bytearray(c1)
    c2 = bytearray(c2)
    p2 = bytearray([0]*16)
    c1_orig = bytearray(c1)
    
    known = b''
    for index in range(1,17):
        c1 = do_padding(c1_orig, known)
        for i in range(0,256):
            c1[0-index] = i
            if oracle(c1, c2):
                known = bytes([i^index^c1_orig[0-index]]) + known
                break
                    
    return known
    
def padding_oracle_attack(ciphertext, oracle):
    def padding_oracle(c1, c2):
        token = b"".join([c1,c2])
        try: return oracle(token)
        except: return False
            
    blocks = to_blocks(ciphertext, 16)
    known = b''
    for i in range(len(blocks)-1):
        known += padding_oracle_block(blocks[i], blocks[i+1], padding_oracle)
   
    return known
    
    
token = gen_token()
print(unpad(padding_oracle_attack(token, check_token)).decode("ascii"))














