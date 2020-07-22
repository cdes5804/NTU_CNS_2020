import string
from pwn import *
import binascii
from Cryptodome.Util.number import bytes_to_long, long_to_bytes
from Cryptodome.Util.Padding import pad, unpad

def flag1(s, cipher, mac):
    s.sendlineafter('>', '3'.encode())
    s.sendlineafter(':', '||'.join([cipher, mac]).encode())
    n = int(s.recvline().decode().split('=')[1].strip())
    s.sendlineafter('>', '1'.encode())
    s.sendlineafter(':', '02'.encode())
    enc = int(s.recvline().decode())
    m = int(cipher) * enc % n
    s.sendlineafter('>', '2'.encode())
    s.sendlineafter(':', str(m).encode())
    res = s.recvline().decode().strip()
    flag1 = long_to_bytes(bytes_to_long(binascii.unhexlify(res)) // 2).decode()
    return flag1

def flag2(s, cipher, mac, flag):
    bts = bytes_to_long(binascii.unhexlify(mac))
    m = bytes_to_long(pad(flag.encode(), 16))
    stream = m ^ bts
    newstr = flag[:-4] + 'getflag'
    nm = pad(newstr.encode(), 16)
    mac = binascii.hexlify(long_to_bytes(bytes_to_long(nm) ^ stream))
    s.sendlineafter('>', '1'.encode())
    s.sendlineafter(':', binascii.hexlify(newstr.encode()))
    message = s.recvline().decode().strip()
    s.sendlineafter('>', '3'.encode())
    s.sendlineafter(':', (message + '||' + mac.decode()).encode())
    flag2 = s.recvline().decode().strip()
    return flag2
    


s = remote('cns.csie.org', 10201)
cipher, mac = s.recvline().decode().split(':')[1].strip().split('||')
f1 = flag1(s, cipher, mac)
f2 = flag2(s, cipher, mac, f1)
print(f1)
print(f2)