#!/usr/bin/python3
# Author: how2hack
# Requirement: pip3 install --user pycryptodomex
#

from binascii import hexlify, unhexlify

from Cryptodome.Cipher import AES, PKCS1_v1_5
from Cryptodome.PublicKey import RSA
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Random import get_random_bytes
import Cryptodome.Util.number
from Cryptodome.Util.number import ceil_div, bytes_to_long, long_to_bytes

import secret

class Enc:
    def __init__(self):
        self.key = RSA.generate(1024)
        self.macKey = get_random_bytes(32)
        self.iv = get_random_bytes(16)
        self.prefix = secret.FLAG1
        self.mode = 0
        self.bonus = 1

    def mac(self, msg):
        aes = AES.new(self.macKey, AES.MODE_OFB, self.iv)
        mac = aes.encrypt(pad(msg, 16))
        return hexlify(mac)

    def unmac(self, msg):
        aes = AES.new(self.macKey, AES.MODE_OFB, self.iv)
        mac = aes.decrypt(unhexlify(msg))
        return unpad(mac, 16)

    def encrypt(self, msg):
        if self.mode == 0:
            return self.key._encrypt(bytes_to_long(msg))
        else:
            cipher = PKCS1_v1_5.new(self.key)
            return bytes_to_long(cipher.encrypt(msg))

    def decrypt(self, msg):
        if self.mode == 0:
            return long_to_bytes(self.key._decrypt(msg))
        else:
            cipher = PKCS1_v1_5.new(self.key)
            sentinel = None
            try:
                plaintext = cipher.decrypt(long_to_bytes(msg), sentinel)
            except:
                return None

            return plaintext

    def info(self):
        print(f'n = {self.key.n}')
        print(f'e = {self.key.e}')

    def get_flag2(self):
        print(f'{secret.FLAG2}')

    def change_mode(self):
        self.mode = 1

    def get_bonus(self):
        if self.mode == 0 or self.bonus == 0:
            print('Nope')
        else:
            self.bonus = 0
            nonce = bytes_to_long(get_random_bytes(8))
            msg = f'{self.prefix}||{nonce}||{secret.FLAG3}'
            msg = msg.encode()
            ciphertext = self.encrypt(msg)
            print(f'Bonus Flag: {ciphertext}')

    def get_info_cmd(self):
        nonce = bytes_to_long(get_random_bytes(8))
        msg = f'{self.prefix}||{nonce}||info'
        msg = msg.encode()
        mac = self.mac(msg).decode()
        ciphertext = self.encrypt(msg)
        print(f'Use this command to get info: {ciphertext}||{mac}')

    def cmd(self, c):
        data = c.split('||')
        if len(data) != 2:
            print('Invalid Format')
            return
        try:
            msg = self.decrypt(int(data[0]))
        except:
            print('Something went wrong')
            return
        mac = self.unmac(data[1])
        if msg == mac:
            msg = msg.split(b'||')
            if len(msg) != 3:
                print('Invalid Command Format')
                return
            if msg[0] == self.prefix.encode():
                if msg[2] == b'info':
                    self.info()
                elif msg[2] == b'getflag':
                    self.get_flag2()
                elif msg[2] == b'mode':
                    self.change_mode()
                elif msg[2] == b'bonus':
                    self.get_bonus()
                else:
                    print('Command Not Found')
            else:
                print('Unauthorized')
        else:
            print('Invalid Command')
