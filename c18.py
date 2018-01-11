#!/usr/bin/env python3

from binascii import hexlify, unhexlify
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from c05 import xorstr
from c06 import to_blocks
import struct

def aes_ctr(key, nonce, data):
    crypt = AES.new(key, AES.MODE_ECB)
    blocks = to_blocks(data, 16)
    plaintext = b''
    for i in range(0, len(blocks)):
        f = struct.pack("<qq", nonce, i)
        k = crypt.encrypt(f)
        plaintext += xorstr(blocks[i], k)
    return plaintext

if __name__ == "__main__":
    ciphertext = b"L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=="
    ciphertext = b64decode(ciphertext)
    plaintext = aes_ctr("YELLOW SUBMARINE", 0, ciphertext)
    print(plaintext.decode("ascii"))

        
