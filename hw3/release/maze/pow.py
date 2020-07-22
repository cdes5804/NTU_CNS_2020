#!/usr/bin/env python
# Author: how2hack
# Requirement: None
# 

import sys
import hashlib

def sha256(m):
    h = hashlib.sha256()
    h.update(m)
    return h.hexdigest()

if __name__ == '__main__':
    nonce = sys.argv[1]
    level = int(sys.argv[2])
    
    i = 0

    while True:
        if (int(sha256(nonce+str(i)), 16) % (2 ** level)) == 0:
            print i
            break
        i += 1