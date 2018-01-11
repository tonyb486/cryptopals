#!/usr/bin/env python3

import math
from binascii import hexlify, unhexlify
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Random import random
from Crypto import Random
from urllib.parse import parse_qsl, urlencode

from c06 import to_blocks
from c09 import pad_pkcs7
from c11 import detect_mode

rndfile = Random.new()
key = rndfile.read(16)

def parse_kv(string):
    return dict(parse_qsl(string))
    
def profile_for(email):
    profile = {"email": email, "uid": 10, "role": "user"}
    return urlencode(profile)


def encrypted_profile_for(email):
    global key
    crypt = AES.new(key, AES.MODE_ECB)
    return crypt.encrypt(pad_pkcs7(profile_for(email).encode("ascii"), 16))

def decode_profile(payload):
    global key
    crypt = AES.new(key, AES.MODE_ECB)
    return parse_kv(crypt.decrypt(payload))

#################################################################################3

def get_blocksize_and_boundry(enc_function):
    size = len(enc_function(b""))
    for i in range(50):
        new_size = len(enc_function(b"A"*i))
        if new_size > size:
            return i, (new_size - size)

# Boundry is how far we have to go to force it into a new block
#
# "email=AAAAAAAAAA|&uid=10&role=use|r

boundry, blocksize = get_blocksize_and_boundry(encrypted_profile_for)

# Everything after boundry gets put into a new block, so we can control
# a whole block this way, in this case, our block will be "admin&uid=10&rol"
# which is close enough for urldecoding!
#
# "email=AAAAAAAAAA|admin&uid=10&rol|e=user

payload = (b"A"*boundry) + b"admin"
admin_block = to_blocks(encrypted_profile_for(payload), blocksize)[1]

# Now we push off just enough to get the "user" alone in the last block
# So, "A"*(len("user"))-1 will do exactly that, and give us:
#
# "email=AAAAAAAAAA|AAA&uid=10&role=|user

payload = b'A'*(boundry+len("user")-1)
blocks = to_blocks(encrypted_profile_for(payload), blocksize)[:-1]

# Then, swap the last block with our new one that starts with "admin"
#
# "email=AAAAAAAAAA|AAA&uid=10&role=|admin&uid=10&rol

blocks.append(admin_block)
modified_payload = b"".join(blocks)

# Bingo bongo!
print(decode_profile(modified_payload))



