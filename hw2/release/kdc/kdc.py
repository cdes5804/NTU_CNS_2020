#!/usr/bin/python3 -uB
# Author: how2hack
# Requirement: pip3 install --user pycryptodomex
# nc cns.csie.org 10220

import os
from binascii import hexlify
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.number import bytes_to_long

import util
import secret

def register(name):
    if not name.isalnum():
        print('Nope')
        return None
        
    keys = os.listdir(secret.key_path)

    if name in keys:
        print('User exists')
        return None
    else:
        kE = hexlify(get_random_bytes(32)).decode()
        kM = hexlify(get_random_bytes(32)).decode()
        with open(os.path.join(secret.key_path, name), 'w') as f:
            f.write(kE + '\n')
            f.write(kM + '\n')
        return kE, kM

def key_exchange(n1, n2, id1, id2):
    kp1 = os.path.join(secret.key_path, id1)
    kp2 = os.path.join(secret.key_path, id2)

    if not os.path.exists(kp1) or not os.path.exists(kp2):
        print('User not found')
        exit(-1)

    kE1, kM1 = util.get_key(kp1)
    kE2, kM2 = util.get_key(kp2)

    shareKey = hexlify(get_random_bytes(32))

    c2 = util.encrypt(kE2, shareKey)
    d2 = f'{id1}||{n1}||{n2}'
    t2 = util.mac(kM2, d2.encode())

    c1 = util.encrypt(kE1, shareKey)
    d1 = f'{id2}||{n1}||{n2}'
    t1 = util.mac(kM1, d1.encode())

    return c1, t1, c2, t2
    
def admin(name):
    kp = os.path.join(secret.key_path, name)
    if not os.path.exists(kp):
        print('User not found')
        exit(-1)

    kE, kM = util.get_key(kp)
    nonce = bytes_to_long(get_random_bytes(16))
    print(f'Nonce: {nonce}')
    ticket = input('Ticket: ').strip()

    data = f'{name}||{nonce}'
    if ticket != util.mac(kM, data.encode()):
        print('Unauthorized')
        exit(-1)

    if name == 'Admin':
        return util.encrypt(kE, secret.FLAG2)
    else:
        msg = f'Hello guest, {name}'
        return util.encrypt(kE, msg.encode())

def menu():
    print("=================")
    print(" 1. Register     ")
    print(" 2. Key Exchange ")
    print(" 3. Admin Login  ")
    print("=================")

if __name__ == "__main__":
    menu()
    choice = input('> ').strip()
    try:
        choice = int(choice)
    except:
        exit(-1)

    if choice == 1:
        name = input('Name: ').strip()
        print(register(name))
    elif choice == 2:
        n1, n2, id1, id2 = input('Data: ').strip().split('||')
        print(key_exchange(n1, n2, id1, id2))
    elif choice == 3:
        name = input('Name: ').strip()
        print(admin(name))
    else:
        exit(-1)
