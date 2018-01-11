#!/usr/bin/env python3

from binascii import hexlify, unhexlify
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from c06 import to_blocks

def detect_ecb(data, blocksize):
    blocks = to_blocks(data, 16)
    if len(blocks) != len(set(blocks)):
        return True
    return False

if __name__ == "__main__":
    # Read the data from the file
    data = [unhexlify(i.strip()) for i in open("c08_data.txt").readlines()]

    for i in data:
        if detect_ecb(i,16):
            print("ECB Detected!")
            print(hexlify(i))

