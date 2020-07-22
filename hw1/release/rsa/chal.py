#!/usr/bin/python3 -uB
# Author: how2hack
# Requirement: pip3 install --user pycryptodomex
#

import signal
from enc import Enc
from binascii import hexlify, unhexlify

def handler(signum, frame):
    print('AFK for too long')
    exit(-1)

def menu():
    print('===============')
    print(' 1. Encrypt    ')
    print(' 2. Decrypt    ')
    print(' 3. Command    ')
    print(' 4. Exit       ')
    print('===============')

if __name__ == "__main__":
    signal.signal(signal.SIGALRM, handler)
    enc = Enc()
    enc.get_info_cmd()

    while True:
        menu()
        signal.alarm(60)
        choice = input('> ').strip()
        try:
            choice = int(choice)
        except:
            print('Invalid Choice')
            continue

        if choice == 1:
            msg = input('Message (in hex): ').strip()
            msg = unhexlify(msg)
            emsg = enc.encrypt(msg)
            if emsg:
                print(emsg)

        elif choice == 2:
            msg = input('Message: ').strip()
            try:
                msg = int(msg)
            except:
                print('Invalid Message')
                continue
            dmsg = enc.decrypt(msg)
            if dmsg == None:
                print('Error')
                continue
            if enc.prefix.encode() not in dmsg:
                print(hexlify(dmsg).decode())
            else:
                print('Nope')

        elif choice == 3:
            cmd = input('Command: ').strip()
            enc.cmd(cmd)

        elif choice == 4:
            break

        else:
            print('Invalid Choice')
