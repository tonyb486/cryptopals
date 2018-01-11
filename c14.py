#!/usr/bin/env python3

import math
from binascii import hexlify, unhexlify
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Random import random
from Crypto import Random
from c09 import pad_pkcs7
from c06 import to_blocks
from c11 import detect_mode

magic = b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg"+
                  "aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq"+
                  "dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg"+
                  "YnkK")

rndfile = Random.new()
key = rndfile.read(16)
prefix=rndfile.read(random.randrange(0,21))

def encryption_oracle(data):
    global key, prefix
    crypt = AES.new(key, AES.MODE_ECB)
    
    return crypt.encrypt(pad_pkcs7(prefix+data+magic, 16))

def get_blocksize(enc_function):
    size = len(enc_function(b""))
    for i in range(50):
        new_size = len(enc_function(b"A"*i))
        if new_size > size:
            return new_size - size

def get_boundry(enc_function, blocksize):
    for i in range(blocksize,blocksize*3):
        b = to_blocks(enc_function(b"A"*i), blocksize)
        for x in range(len(b)-1):
            if b[x]==b[x+1]: 
                return (x+2)*blocksize, i

def get_ptsize(enc_function):
    size = len(enc_function(b""))
    for i in range(50):
        new_size = len(enc_function(b"A"*i))
        if new_size > size:
            return size - i + 1

def ecb_decrypt_oracle_chosen_middle(enc_function):
    # First, determine that it is indeed ECB
    assert detect_mode(enc_function) == AES.MODE_ECB

    # Next, get the blocksize and boundry to our box
    blocksize = get_blocksize(enc_function)

    # Figure out how much off the beginning to ignore,
    # and how many "A"s to pad it with to make it ignorable
    ignore, padding = get_boundry(enc_function, blocksize)
    
    # Now that we know how much to prepend to make it start at a boundry
    # we can use identical code, just prepend it to the plaintext and chop it
    # off from the ciphertext, and it's the same as a prefix!    
    enc_padded = lambda x: enc_function((b"A"*padding)+x)[ignore:]
    
    # Get the size of the plaintext, and the nearest block boundry
    ptsize = get_ptsize(enc_padded)
    nblen = len(enc_padded(b''))

    known = b""
    while len(known)<ptsize:

        # Encrypt AA...AA[KNOWN][?][BLOCK BOUNDRY]
        payload = b"A"*(nblen-len(known)-1)
        first_block = enc_padded(payload)[0:nblen]

        # Encrypt AA..AA[KNOWN][0-255][BLOCK BOUNDRY]
        # When it matches, we know the last bytes are the same!
        for i in range(0, 255):
            payload = b"A"*(nblen-len(known)-1)+known+bytes([i])
            new_first_block = enc_padded(payload)[0:nblen]
            if new_first_block == first_block: 
                known = known+bytes([i])
                break
                
    return known
    
    
if __name__ == "__main__":
    print(ecb_decrypt_oracle_chosen_middle(encryption_oracle).decode("ascii"))




