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
	"""Get all primes up to a certain number using a sieve and a little caching magic"""
	if sieve_to.prime_cache[len(sieve_to.prime_cache) - 1] >= n+1:
		prime_list = []
		for i in sieve_to.prime_cache:
			if i > n + 1:
				break
			prime_list.append(i)
		return prime_list

	l = sieve_to.prime_cache + list(range(sieve_to.prime_cache[len(sieve_to.prime_cache) - 1] + 1, n+1))
	for n in l:
		for i in l[l.index(n):]:
			if i == n:
				continue
			if i % n == 0:
				del l[l.index(i)]  # This *might* run in linear time all on its own... whoops

	# Place newly calculated prime list in the cache
	if len(l) > len(sieve_to.prime_cache):
		sieve_to.prime_cache = l
	return l
sieve_to.prime_cache = [2, 3, 5, 7]


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

for m in range(1, 101):
	for n in range(1, 101):
		if gcd_euclid(m, n) != gcd_middleschool(m, n):
			print(str(m) + ", " + str(n) + " failed to validate")
