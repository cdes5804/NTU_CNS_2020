from scipy.interpolate import lagrange
import binascii
import numpy as np

def _extended_gcd(a, b):
    """
    Division in integers modulus p means finding the inverse of the
    denominator modulo p and then multiplying the numerator by this
    inverse (Note: inverse of A is B such that A*B % p == 1) this can
    be computed via extended Euclidean algorithm
    http://en.wikipedia.org/wiki/Modular_multiplicative_inverse#Computation
    """
    x = 0
    last_x = 1
    y = 1
    last_y = 0
    while b != 0:
        quot = a // b
        a, b = b, a % b
        x, last_x = last_x - quot * x, x
        y, last_y = last_y - quot * y, y
    return last_x, last_y

def _divmod(num, den, p):
    """Compute num / den modulo prime p

    To explain what this means, the return value will be such that
    the following is true: den * _divmod(num, den, p) % p == num
    """
    inv, _ = _extended_gcd(den, p)
    return num * inv

def _lagrange_interpolate(x, x_s, y_s, p):
    """
    Find the y-value for the given x, given n (x, y) points;
    k points will define a polynomial of up to kth order.
    """
    k = len(x_s)
    assert k == len(set(x_s)), "points must be distinct"
    def PI(vals):  # upper-case PI -- product of inputs
        accum = 1
        for v in vals:
            accum *= v
        return accum
    nums = []  # avoid inexact division
    dens = []
    for i in range(k):
        others = list(x_s)
        cur = others.pop(i)
        nums.append(PI(x - o for o in others))
        dens.append(PI(cur - o for o in others))
    den = PI(dens)
    num = sum([_divmod(nums[i] * den * y_s[i] % p, dens[i], p)
               for i in range(k)])
    return (_divmod(num, den, p) + p) % p

f = open('parameter', 'r')
par = [0 for _ in range(6)]
counter = 0
for line in f:
	par[counter] = int(line.split()[2])
	counter += 1

def getc(n):
	filename = f'D{n}'
	f = open(filename, 'r')
	for line in f:
		number = int(line.split(',')[1])
		if pow(par[2], number, par[0]) == par[3] * par[4]**(n) * par[5]**(n*n) % par[0]:
			return number
	return 0

A = []
for i in range(1, 4):
	A.append(getc(i))
result = lagrange(list(range(1, 4)), A)
num = _lagrange_interpolate(0, list(range(1, 4)), A, par[1])
print(bytearray.fromhex(str(hex(num))[2:]).decode('UTF-8'))
