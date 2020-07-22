import string
from pwn import *
import binascii
import csv
from Cryptodome.Cipher import ARC4

def get_packet():
    fs, ivs = [], []
    for _ in range(22000):
        print(_)
        s = remote('cns.csie.org', 10203)
        message = s.recvline().decode().split('||')
        iv = binascii.unhexlify(message[0])
        content = binascii.unhexlify(message[1].strip())
        if iv[0] >= 3:
            ivs.append([iv, content])
            fs.append(f'{iv[0]}, {iv[1]}, {iv[2]}, {content[0]}')
        s.close()
    csv.writer(open('data', 'w')).writerows(sorted(fs))
    return sorted(ivs)

def initSBox(box):
    for i in range(256): box[i] = i

def decrypt(key, ivs):
    f = open('result', 'w')
    for iv in ivs:
        cipher = ARC4.new(iv[0] + key.encode())
        print(cipher.decrypt(iv[1]).decode(), file=f)


def find_key(ivs):
    key_length = int(ivs[-1][0][0]) - 2
    print(key_length)
    key = [None] * 3
    plainSNAP = "48"
    box = [i for i in range(256)]
    for A in range(key_length):
        prob = [0] * 256
        for iv in ivs:
            key[0], key[1], key[2] = int(iv[0][0]), int(iv[0][1]), int(iv[0][2])
            j = 0
            initSBox(box)

            for i in range(A + 3):
                j = (j + box[i] + key[i]) % 256
                box[i], box[j] = box[j], box[i]
                if i == 1:
                    original0 = box[0]
                    original1 = box[1]

            i = A + 3
            z = box[1]
            if z + box[z] == A + 3:
                if (original0 != box[0] or original1 != box[1]):
                    continue
                keyStreamByte = int(iv[1][0]) ^ int(plainSNAP, 16)
                keyByte = (keyStreamByte - j - box[i]) % 256
                prob[keyByte] += 1
            higherPossibility = prob.index(max(prob))
        key.append(higherPossibility)

    res = key[3:]
    result = [format(key, 'x') for key in res]
    rawkey = ''.join(result).upper()
    return binascii.unhexlify(rawkey).decode()




ivs = get_packet()
key = find_key(ivs)
print(key)
decrypt(key, ivs)
