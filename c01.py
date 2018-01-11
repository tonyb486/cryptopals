#!/usr/bin/env python3

import binascii
from base64 import b64encode, b64decode


data = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
data = binascii.unhexlify(data)
b64 = b64encode(data).decode("utf-8")

assert b64 == "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"

print(data.decode("utf-8"))
