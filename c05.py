#!/usr/bin/env python3

from binascii import hexlify, unhexlify
from base64 import b64encode, b64decode

def xorstr(string, key):
    return bytes([string[i]^key[i%len(key)] for i in range(len(string))])

if __name__ == "__main__":
    plaintext = b"Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    ciphertext = xorstr(plaintext, b"ICE")
    print(hexlify(ciphertext).decode("ascii"))
    assert hexlify(ciphertext) == b"0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"
 

