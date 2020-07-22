#!/usr/bin/python3
# Author: how2hack
# Requirement: pip3 install --user pycryptodomex
#

from binascii import hexlify, unhexlify
from Cryptodome.Cipher import Salsa20
from Cryptodome.Hash import SHA256, HMAC

def encrypt(key, msg):
    cipher = Salsa20.new(key=key)
    return hexlify(cipher.nonce + cipher.encrypt(msg)).decode()

def decrypt(key, msg):
    msg = unhexlify(msg.encode())
    nonce = msg[:8]
    c = msg[8:]
    cipher = Salsa20.new(key=key, nonce=nonce)
    return cipher.decrypt(c)

def mac(key, msg):
    h = HMAC.new(key, digestmod=SHA256)
    h.update(msg)
    return h.hexdigest()

def get_key(p):
    kE, kM = open(p).read().strip().split('\n')
    kE = unhexlify(kE.encode())
    kM = unhexlify(kM.encode())
    return kE, kM