#!/usr/bin/python3 -uB
# Author: how2hack
# Requirement: pip3 install --user pycryptodomex
#

import random
from binascii import hexlify, crc32

from Cryptodome.Cipher import ARC4

import secret

class WEP:
    def __init__(self):
        self.key = secret.key
    
    def encrypt(self, msg):
        crc = crc32(msg)
        p = f'{msg.decode()}||{crc}'
        iv = secret.random_three_bytes()
        key = iv+self.key
        cipher = ARC4.new(key)
        enc = cipher.encrypt(p.encode())
        c = f'{hexlify(iv).decode()}||{hexlify(enc).decode()}'
        return c

if __name__ == "__main__":
    wep = WEP()
    print(wep.encrypt(random.choice(secret.msg)))
