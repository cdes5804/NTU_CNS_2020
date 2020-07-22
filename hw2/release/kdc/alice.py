#!/usr/bin/python3 -uB
# Author: how2hack
# Requirement: pip3 install --user pycryptodomex
# nc cns.csie.org 10221

import os
import util
import user
import secret

NAME = 'Alice'

def menu():
    print("=================")
    print(" 1. Connect      ")
    print(" 2. Accept       ")
    print("=================")

if __name__ == "__main__":
    kp = os.path.join(secret.key_path, NAME)
    u = user.User(NAME, kp)
    menu()
    choice = input('> ').strip()
    try:
        choice = int(choice)
    except:
        exit(-1)

    if choice == 1:
        _id, skey = u.connect()
        print(f'Connected with {_id}')
        if _id == 'Bob':
            print(util.encrypt(skey, secret.FLAG1))
        else:
            msg = f'Hi, {_id}'
            print(util.encrypt(skey, msg.encode()))
    elif choice == 2:
        _id, skey = u.accept()
        print(f'Connected with {_id}')
        msg = f'Hi, {_id}'
        print(util.encrypt(skey, msg.encode()))
    else:
        exit(-1)
