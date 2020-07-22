#!/usr/bin/python3
# Author: how2hack
# Requirement: pip3 install --user pycryptodomex
#

from binascii import unhexlify
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.number import bytes_to_long

import kdc
import util

class User:
    def __init__(self, name, kp):
        self.name = name
        self.kE, self.kM = util.get_key(kp)
    
    def connect(self):
        n = bytes_to_long(get_random_bytes(16))
        data = f'{n}||{self.name}'
        print(data)

        _c, _t, _id, _n = input().strip().split('||')
        if _id == self.name:
            exit(-1)
        d = f'{_id}||{n}||{_n}'
        t = util.mac(self.kM, d.encode())

        if t != _t:
            print('Invalid tag')
            exit(-1)
        
        skey = unhexlify(util.decrypt(self.kE, _c))

        return _id, skey

    def accept(self):
        _n, _id = input().strip().split('||')
        if _id == self.name:
            exit(-1)

        n = bytes_to_long(get_random_bytes(16))
        c1, t1, c2, t2 = kdc.key_exchange(_n, n, _id, self.name)
        
        d = f'{_id}||{_n}||{n}'
        t = util.mac(self.kM, d.encode())

        if t != t2:
            print('Invalid tag')
            exit(-1)

        print(f'{c1}||{t1}||{self.name}||{n}')

        skey = unhexlify(util.decrypt(self.kE, c2))

        return _id, skey
