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


rndfile = Random.new()
key = rndfile.read(16)

def gen_token(userdata):
    global key
    iv = rndfile.read(16)
    crypt = AES.new(key, AES.MODE_CBC, iv)
    userdata = userdata.replace(b"=", b"") # OM NOM NOM
    userdata = userdata.replace(b";", b"") # NOM NOM NOM NOM
    data = b"comment1=cooking%20MCs;userdata="+userdata+b";comment2=%20like%20a%20pound%20of%20bacon"
    return iv+crypt.encrypt(pad_pkcs7(data, 16))

def check_admin(token):
    global key
    crypt = AES.new(key, AES.MODE_CBC, token[0:16])    
    plaintext = unpad(crypt.decrypt(token[16:])) # oh no, padding oracles! (for later)
    pairs = [i.rsplit(b"=") for i in plaintext.rsplit(b";")]

    return ([b"admin", b"true"] in pairs)
    
##########################################################

# Generate a token, what is in it doesn't really matter the way we're
# doing it, since we know what lives in the last block - let's just make it
# "TOKEN," because that makes us land on an even padding :)
token = gen_token(b"TOKEN")

# The last two blocks are going to be filled with, like, a pound of bacon
# so we know what they are, and we know we can edit them at will without
# really breaking anything important.  

blocks = to_blocks(token, 16)
bits_to_flip = xorstr(b";admin=true;A=A\x01", b"nd%20of%20bacon\x01")
blocks[-2] = xorstr(blocks[-2], bits_to_flip)

token = b"".join(blocks)

print(check_admin(token))
