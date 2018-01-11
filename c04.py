#!/usr/bin/env python3

from binascii import hexlify, unhexlify
from base64 import b64encode, b64decode

from c03 import frequency_sum, frequency_error_chi2

if __name__ == "__main__":
    data = open("c04_data.txt").readlines()
    scores = []
    for i in data:
        ciphertext = unhexlify(i.strip())
        for b in range(0, 255):
            plaintext = bytes([b^i for i in ciphertext])    
            scores.append((frequency_sum(plaintext),b,plaintext, ciphertext))  

    scores = sorted([i for i in scores if i[0]>=0], key = lambda x: x[0])
    print(scores[-1][2].decode("ascii"))
