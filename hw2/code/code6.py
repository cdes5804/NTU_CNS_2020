import math
from Crypto.PublicKey import RSA

bob = '6d:68:8e:5d:c2:27:96:18:8f:e5:e1:c5:ce:d9:d8:\
49:08:aa:a2:91:fa:5e:42:2b:cc:f5:64:fb:80:bd:\
32:39:53:e7:fb:c5:6e:4e:83:24:f5:5f:07:32:92:\
34:31:ee:cc:b7:6d:53:2f:69:e2:29:d4:01:18:45:\
26:98:3a:eb:e8:d9:68:cb:2a:98:bd:a1:40:cc:fb:\
d5:9e:97:a9:28:e0:c3:b3:a7:3f:89:d2:2c:0e:40:\
fe:1a:63:b0:e9:d8:79:8b:af:53:a5:0d:f7:e9:f3:\
41:d0:fd:6b:a5:5c:af:ac:19:b4:16:eb:0e:42:e3:\
64:41:ea:c0:16:16:bb:df:6a:13:bc:1b:04:4c:0f:\
e4:70:56:a6:49:4a:a7:d4:fe:07:b9:a4:df:b1:f6:\
6c:17:50:39:eb:c1:7c:fb:50:1a:61:aa:08:d7:8a:\
96:ae:0e:37:1f:5f:ca:2f:87:5c:cd:a3:4e:11:54:\
2f:c9:2b:0f:45:08:d6:9c:9c:d7:91:88:2e:87:8d:\
1d:2d:0c:e8:06:99:eb:fb:40:bd:0a:d7:f0:bd:c0:\
01:70:6a:c5:18:66:d1:c4:45:b6:eb:09:00:18:bc:\
8e:60:0f:92:80:f3:5a:8a:df:42:27:a8:a9:4a:67:\
a6:eb:96:fd:3b:bc:7a:62:cb:b3:da:4f:b1:bf:9e:\
45'

bob = int(''.join(bob.split(':')), 16)

def sqrt_ceil(n):
    left, right, ans = 1, n, 0
    while left <= right:
        mid = (left + right) // 2
        if mid**2 >= n:
            ans = mid
            right = mid - 1
        else: left = mid + 1
    return ans

def is_sqrt(n):
    m = sqrt_ceil(n)
    return m**2 == n

def fermat(n):
    a = sqrt_ceil(n)
    b = a**2 - n
    while not is_sqrt(b):
        a += 1
        b = a**2 - n
    return a - sqrt_ceil(b), a + sqrt_ceil(b)

def modinv(base, mod):
    a, b, c, d = 1, base, 0, mod
    iter = 1
    while d:
        q = b // d
        r = b % d
        t = a + q * c
        a, c, b, d = c, t, d, r
        iter *= -1
    return mod - a if iter < 0 else a

p, q = fermat(bob)
mod = (p - 1) * (q - 1)
e = 65537
d = modinv(e, mod)
rsa = RSA.construct((bob, e, d, p, q))
print(rsa.exportKey().decode())
