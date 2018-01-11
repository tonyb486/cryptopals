#!/usr/bin/env python3

from binascii import hexlify, unhexlify
from base64 import b64encode, b64decode
from c05 import xorstr
from c03 import break_single_xor

def hamming_distance(s1, s2):
    assert len(s1) == len(s2)

    # List comprehensions are fun!
    xor = [s1[i] ^ s2[i] for i in range(len(s1))]
    xor_bin = [ (i>>x)&1 for x in range(7,-1,-1) for i in xor]
    
    return sum(xor_bin)

def get_keysizes(data, iterations):
    keysizes = []
    for keysize in range(2, 40):  
       score = 0  
       for i in range(iterations): 
            score += hamming_distance(data[keysize*i:keysize*(i+1)], data[keysize*(i+1):keysize*(i+2)])
       score = (score/iterations)/keysize
        
       keysizes.append( (keysize, score) )

    return [i[0] for i in sorted(keysizes, key=lambda x: x[1])]
  
def to_blocks(data, blocksize):
    return [data[i:i+blocksize] for i in range(0, len(data), blocksize)]

def transpose(blocks, blocksize):
    return [bytes([x[i] for x in blocks if len(x)>i]) for i in range(blocksize)]


if __name__ == "__main__":
    data = b64decode(open("c6_data.txt").read())
    keysize = get_keysizes(data, 10)[0]

    print("Using keysize %d" % keysize)

    blocks = to_blocks(data, keysize)
    blocks = transpose(blocks, keysize)

    key = bytes([break_single_xor(i) for i in blocks])
    print("Using key '%s'\n=========================================" % key.decode("ascii"))

    print(xorstr(data, key).decode("ascii"))








