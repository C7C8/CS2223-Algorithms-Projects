#!/usr/bin/python
def gcd_euclid(m, n):
	"""Implementation of Euclid's algorithm for finding a GCD"""
	while n != 0:
		r = m % n
		m = n
		n = r
	return m


def gcd_consec(m, n):
	"""Implementation of the consecutive GCD algorithm"""
	t = min(m, n)
	while t != 0:
		if m % t == 0:
			if n % t == 0:
				return t
		t -= 1
	return 1


def sieve_to(n):
	"""Simple sieving algorithm to get all primes up to the specified number"""
	l = list(range(2, n))
	for n in l:
		for i in l:
			if i == n:
				continue
			if i % n == 0:
				del l[l.index(i)]
	return l

print(sieve_to(100))
