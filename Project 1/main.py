#!/usr/bin/python
from matplotlib import pyplot as plt, style
import timeit
import random
import csv


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
	i = 0
	while i < len(l): # Can't use regular range()-based loops here
		j = i+1
		while j < len(l):
			if l[j] % l[i] == 0:
				del l[j]
				j -= 1
			j += 1
		i += 1

	# Place newly calculated prime list in the cache
	if len(l) > len(sieve_to.prime_cache):
		sieve_to.prime_cache = l
	return l
sieve_to.prime_cache = [2, 3, 5, 7]


def factor(n):
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
	"""Find the GCD of two numbers using the middleschool algorithm"""
	mfactors = factor(m)
	nfactors = factor(n)
	factors = []

	# Obtain list intersection between mfactors and nfactors
	i = j = 0
	while i != len(mfactors) and j != len(nfactors):
		if mfactors[i] == nfactors[j]:
			factors.append(mfactors[i])
		elif mfactors[i] < nfactors[j]:
			j -= 1
		elif nfactors[j] < mfactors[i]:
			i -= 1

		i += 1
		j += 1

	prod = 1
	for f in factors:
		prod *= f

	return prod


def gcd_wrapper(algo, m, n):
	"""Wrapper needed so that timeit does what I need it to"""
	def wrapped():
		return algo(m, n)
	return wrapped

size = 250
sieve_to(size)
data = [[0.0]*size for i in range(0, size)]
mx = -1.0
for i in range(0, size):
	if i % 5 == 0:
		print("%d/%d" % (i, size))
	for j in range(0, size):
		if i == j:
			continue
		data[i][j] = timeit.timeit(gcd_wrapper(gcd_consec, i, j), number=10)
		if data[i][j] > mx:
			mx = data[i][j]

# Normalize
for i in range(0, size):
	for j in range(0, size):
		data[i][j] /= mx

figure, ax = plt.subplots()
ax.imshow(data, extent=[0, size, 0, size], cmap="jet", origin="upper")
ax.set_frame_on(False)
plt.show()
