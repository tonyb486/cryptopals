#!/usr/bin/env python3

from binascii import hexlify, unhexlify
from base64 import b64encode, b64decode
from Crypto.Cipher import AES


data = b64decode(open("c07_data.txt").read())

crypt = AES.new("YELLOW SUBMARINE", AES.MODE_ECB)
print(crypt.decrypt(data).decode("ascii"))







