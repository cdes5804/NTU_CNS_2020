#!/usr/bin/python3 -uB
# Author: how2hack
# Requirement: pip3 install --user pycryptodomex
# The server will run this code every 120 seconds

import os

import kdc
import secret

if __name__ == "__main__":
    keys = os.listdir(secret.key_path)
    for k in keys:
        os.remove(os.path.join(secret.key_path, k))

    kdc.register('Alice')
    kdc.register('Bob')
    kdc.register('Admin')
