#!/usr/bin/python
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
	def wrapped():
		return algo(m, random.randint(2, n))
	return wrapped


def test_gcd_algo(algo, repeat_count, n):
	"""Test an algo on a set of values, each time repeating the algorithm the specified amount of times """

	timings = [0.0 for i in range(0, n)]
	for i in range(1, n):
		timings[i] += timeit.timeit(gcd_wrapper(algo, i, n), number=repeat_count)
	for i in range(0, len(timings)):
		timings[i] /= 2  # each number pair is actually run twice...
	return timings

max_count = int(input("Highest number to test up to: "))
repeat_count = int(input("Number of trials per number: "))
outfile = str(input("Filename to save to: "))

with open(outfile, 'w') as file:
	writer = csv.writer(file)
	results = []
	print("Testing Euclid's algorithm...")
	results.append(test_gcd_algo(gcd_euclid, repeat_count, max_count))
	print("Testing Consecutive Integer Checking algorithm...")
	results.append(test_gcd_algo(gcd_consec, repeat_count, max_count))
	print("Testing Middle School Algorithm... (this may take some time)")
	results.append(test_gcd_algo(gcd_middleschool, repeat_count, max_count))
	print("Done! All results are printed to a CSV file named \"" + outfile + "\"")
	writer.writerow(results)
