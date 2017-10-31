#!/usr/bin/python
from collections import Counter


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
	l = list(range(2, n+1))
	for n in l:
		for i in l[l.index(n):]:
			if i == n:
				continue
			if i % n == 0:
				del l[l.index(i)]  # This *might* run in linear time all on its own... whoops
	return l


def factors_of(n):
	"""Factor a number using a prime finding sieve and a little magic"""
	prime_list = sieve_to(int(n / 2))
	factor_list = []
	temp = n
	for i in prime_list:
		while temp % i == 0 and n != 1:
			factor_list.append(i)
			temp /= i

	if len(factor_list) == 0:
		factor_list.append(n)
	return factor_list

def gcd_middleschool(m, n):
	# What, did you really think I was going to write a list intersection algorithm myself? When one this good
	# already exists?
	factors = list((Counter(factors_of(m)) & Counter(factors_of(n))).elements())
	i = 1
	for factor in factors:
		i *= factor

	return i

for m in range(1, 1001):
	for n in range(1, 1001):
		if gcd_euclid(m, n) != gcd_middleschool(m, n):
			print(str(m) + ", " + str(n) + " failed to validate")
