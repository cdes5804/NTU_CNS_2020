import string
from pwn import *
import binascii

s = remote('cns.csie.org', 10202)

def logout():
	global s
	s.sendlineafter(' : ', '4')

def try_login(token, strict = False, out = True):
	global s
	if s.closed['recv'] == True or s.closed['send'] == True:
		s.close()
		s = remote('cns.csie.org', 10202)
	s.sendlineafter(' : ', '2')
	s.sendlineafter(' : ', binascii.hexlify(token))
	reply = s.recvline().decode().strip()
	if 'menu' in reply:
		if out:
			logout()
		return True
	else:
		if strict: return False
		if 'padding' in reply:
			return False
		else:
			return True

def get_token():
	global s
	s.sendlineafter(':', '1'.encode())
	return s.recvline().decode().split(':')[1].strip()

def decode_block(iv, front, block, cipher = False):
	global s
	crack = [0 for _ in range(16)]
	for i in range(15, -1, -1):
		l = 15 - i + 1
		for k in range(256):
			tmp = bytearray(front[x] ^ crack[x] ^ l for x in range(16)) + block
			tmp[i] ^= k
			if try_login(iv + tmp):
				crack[i] = k
				break
		else:
			print('something went wrong...')
			exit(0)
	if not cipher:
		print(''.join(chr(c) for c in crack))
		return ''.join(chr(c) for c in crack)
	else:
		for i in range(16):
			crack[i] ^= front[i]
		return crack

def flag1(token):
	global s
	token = bytearray(binascii.unhexlify(token.encode()))
	plain = []
	partition = [token[16 * i: 16 * i + 16] for i in range(len(token) // 16)]
	for i in range(1, len(partition)):
		plain.append(decode_block(partition[0], partition[i - 1], partition[i]))
	return ''.join(plain)
	

def find_token(token):
	global s
	token = bytearray(binascii.unhexlify(token.encode()))
	target = bytearray('_wan||isvip:1||i'.encode())
	token[55] ^= 48 ^ 49
	cipher = decode_block(token[:16], token[32: 32+16], token[48: 48+16], cipher = True)
	for i in range(16):
		token[32 + i] = target[i] ^ cipher[i]
	for a in range(255, -1, -1):
		for b in range(255, -1, -1):
			for c in range(255, -1, -1):
				for d in range(255, -1, -1):
					token[32], token[33], token[34], token[35] = a, b, c, d
					if try_login(token, strict = True):
						return token

def flag23(token):
	global s
	token = find_token(token)
	try_login(token, out = False)
	s.sendlineafter(' : ', '1'.encode())
	flag2 = s.recvline().decode().split('!')[1].strip()
	s.sendlineafter('choice : ', '2'.encode())
	flag3 = s.recvline().decode().split(':')[1].strip()
	return flag2, flag3


token = get_token()
print(flag1(token))
s.close()
s = remote('cns.csie.org', 10202)
flag2, flag3 = flag23(token)
print(flag2)
print(flag3)