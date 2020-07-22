import string
import os
import socket
import numpy as np
small = string.ascii_lowercase
big = string.ascii_uppercase

def read_input(sock):
	res = ''
	while True:
		try:
			data = sock.recv(1024)
			if not len(data): break
			res += data.decode()
		except socket.error as e:
			break
	return res

def warmup(s):
	message = read_input(s).split('\n')
	for line in message:
		if 'm1' in line:
			s.sendall((' '.join(line.split()[2:]) + '\n').encode())

def caesar(s, round):
	message = read_input(s).split('\n')
	for line in message:
		if ('c1' if round == 1 or round == 3 else 'c2') in line and '=' in line:
			print(round, line)
			if round != 1:
				for i in range(1, 27):
					t = ''.join(c if c == ' ' else chr(ord('a' if c in small else 'A') +\
				 		(ord(c) - ord('a' if c in small else 'A') + i) % 26) for c in ' '.join(line.split()[3:]))
					print(i, t)
			shift = int(input(f'enter the shift for {round}: ')) if round != 1 else 13
			t = ''.join(c if c == ' ' else chr(ord('a' if c in small else 'A') +\
			 (ord(c) - ord('a' if c in small else 'A') + shift) % 26) for c in ' '.join(line.split()[3:]))
			s.sendall((t + '\n').encode())

def char_map(s):
	message = read_input(s).split('\n')
	c1, m1, c2 = '', '', ''
	for line in message:
		if 'c1' in line: c1 = ' '.join(line.split()[3:])
		elif 'm1' in line: m1 = ' '.join(line.split()[3:])
		elif 'c2' in line: c2 = ' '.join(line.split()[3:])
	mapping = {c.lower(): m.lower() for c, m in zip(c1, m1)}
	res = ''.join('?' if c.lower() not in mapping else mapping[c.lower()].upper() if c.isupper() else mapping[c] for c in c2)
	print(res)
	missing = list(input('enter the missing ones:\n'))[::-1]
	t = ''.join(c if c != '?' else missing.pop() for c in res)
	s.sendall((t + '\n').encode())

def column(s):
	message = read_input(s).split('\n')
	c1, m1, c2 = '', '', ''
	for line in message:
		if 'c1' in line: c1 = line[9:]
		elif 'm1' in line: m1 = line[9:]
		elif 'c2' in line: c2 = line[9:]
	shift = 0
	for i in range(1, len(c1)):
		tmp, cur = '', 0
		for j in range(len(c1)):
			tmp += c1[cur]
			cur = (cur + i) % len(c1)
		if tmp == m1:
			shift = i
			break
	t, cur = '', 0
	for i in range(len(c2)):
		t += c2[cur]
		cur = (cur + shift) % len(c2)
	s.sendall((t + '\n').encode())


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('cns.csie.org', 10200))
s.settimeout(0.2)
warmup(s)
for i in range(1, 4):
	caesar(s, round = i)
char_map(s)
column(s)
message = read_input(s)
print(message)
