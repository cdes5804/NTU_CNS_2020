from pwn import *
from string import ascii_lowercase
from random import seed, choice
import time
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.number import bytes_to_long
from binascii import hexlify, unhexlify
from Cryptodome.Cipher import Salsa20
from Cryptodome.Hash import SHA256, HMAC

def register(name = ''):
    if len(name) == 0: name = ''.join(choice(ascii_lowercase) for _ in range(10))
    try:
        kdc = remote('cns.csie.org', 10220)
    except:
        return None, None, None
    kdc.sendlineafter('>', '1')
    kdc.sendlineafter(': ', name)
    s = kdc.recvline().decode().strip('\n ()').split(',')
    if 'User exists' in s: 
        kdc.close()
        return None, None, None
    ke, km = s[0].strip('\' '), s[1].strip(' \'')
    kdc.close()
    return name, unhexlify(ke.encode()), unhexlify(km.encode())

def get_nonce():
    return bytes_to_long(get_random_bytes(16))

def key_exchange(n1, n2, id1, id2):
    kdc = remote('cns.csie.org', 10220)
    kdc.sendlineafter('>', '2')
    kdc.sendlineafter(': ', '||'.join([str(n1), str(n2), id1, id2]))
    s = kdc.recvline().decode().strip('\n ()').split(',')
    kdc.close()
    c1, t1, c2, t2 = s[0].strip(' \''), s[1].strip(' \''), s[2].strip(' \''), s[3].strip(' \'')
    return c1, t1, c2, t2

def decrypt(key, msg):
    msg = unhexlify(msg.encode())
    nonce = msg[:8]
    c = msg[8:]
    cipher = Salsa20.new(key=key, nonce=nonce)
    return cipher.decrypt(c)

def connect(mode = 'Alice'):
    if mode == 'Alice':
        s = remote('cns.csie.org', 10221)
    elif mode == 'Bob':
        s = remote('cns.csie.org', 10222)
    else: return
    s.sendlineafter('>', '1')
    mesg = s.recvline().decode().strip().split('||')[0]
    return s, mesg

def mac(key, msg):
    h = HMAC.new(key, digestmod=SHA256)
    h.update(msg)
    return h.hexdigest()

def flag1():
    name, k_e, _ = register()
    nonce = get_nonce()
    alice, n_a = connect('Alice')
    c, _, m, _ = key_exchange(n_a, nonce, 'Alice', name)
    skey = unhexlify(decrypt(k_e, m).decode())
    _, t, _, _ = key_exchange(n_a, nonce, 'Alice', 'Bob')
    alice.sendline('||'.join([c, t, 'Bob', str(nonce)]))
    alice.recvline()
    alice.close()
    return decrypt(skey, alice.recvline().decode().strip()).decode()

def login_admin(ke, km):
    admin = remote('cns.csie.org', 10220)
    admin.sendlineafter('>', '3')
    admin.sendlineafter(': ', 'Admin')
    admin.recvuntil('Nonce: ', drop = True)
    nonce = admin.recvline().decode().strip()
    data = mac(km, f'Admin||{nonce}'.encode())
    admin.sendlineafter(': ', data)
    flag = admin.recvline().decode().strip()
    return decrypt(ke, flag).decode()

def flag2():
    while True:
        name, ke, km = register('Admin')
        if name is not None:
            print(f'successfully registered {name}!!!')
            flag = login_admin(ke, km)
            return flag

seed(int(time.time()))
flag = flag1()
print(flag)
flag = flag2()
print(flag)
