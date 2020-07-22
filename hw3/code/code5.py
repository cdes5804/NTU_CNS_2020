import sys
import hashlib
from pwn import *
import subprocess
import os
import time

def sha256(m):
    m = m.encode()
    h = hashlib.sha256()
    h.update(m)
    return h.hexdigest()

def get_parameter(msg):
    sent = msg.split('\n')
    level = int(sent[0].split(' ')[-1])
    nonce = sent[1].split('"')[1]
    return nonce, level

def get_ans(nonce, level):
    i = 0
    while True:
        if int(sha256(nonce+str(i)), 16) % (2**level) == 0: return i
        i += 1

def get_map(s):
    s.sendlineafter('>', '1')
    maze = s.recvline().decode().strip()
    return maze.split()[-1]

def solve_map(maze):
    t = time.time()
    print(maze)
    subprocess.run(['klee', '-exit-on-error', 'maze.bc'], input = maze + '\n', stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL, encoding = 'ascii')
    print(f'run for {time.time() - t} seconds')
    klee_dir = os.path.realpath('klee-last')
    result_file = ''
    for f in os.listdir(klee_dir):
        if f[-3:] == 'err':
            result_file = f.split('.')[0]
            break
    res = subprocess.run(['ktest-tool', f'klee-last/{result_file}.ktest'], stdout = subprocess.PIPE).stdout.decode().strip().split('object 0: text:')[-1].strip().strip('.')
    print(res)
    return res

s = remote('cns-temp.csie.org', 10240)
msg = s.recvuntil('>').decode()
nonce, level = get_parameter(msg)
proof = get_ans(nonce, level)
s.sendline(str(proof))
s.sendlineafter('>', '1')
for i in range(5):
    maze = get_map(s)
    ans = solve_map(maze)
    s.sendlineafter(': ', ans)
    if i == 4:
        for _ in range(2): print(s.recvline().decode())
