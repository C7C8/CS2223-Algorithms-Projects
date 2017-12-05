import sys
from collections import namedtuple
from itertools import chain
from itertools import combinations

def setvals(items):
	"""Calculate the weight and value of a given set"""
	val = weight = 0
	for item in items:
		weight += item[0]
		val += item[1]
	return weight, val


def knapsack_exhaustive(ksize, items):
	"""Conduct exhaustive search by iterating over the power set of the input item list. This is absurdly expensive"""
	powerset = chain.from_iterable(combinations(items, r) for r in range(len(items)+1))
	maxValue = 0
	maxLst = []
	for set in powerset:
		weight,val = setvals(set)
		if val > maxValue and weight <= ksize:
			maxValue = val
			maxLst = set
	return maxValue, maxLst


def knapsack_dp(ksize, items):
	"""Solve knapsack problem using dynamic programming. This algorithm is heavily inspired by the pseudocode for it
	found on Wikipedia... sorry. At least I didn't use CTRL-C/CTRL-V"""
	m = [[0 for i in range(ksize+1)] for j in range(len(items))]
	for i in range(len(items)):
		for j in range(ksize+1):
			if items[i][0] > j:
				m[i][j] = m[i-1][j]
			else:
				m[i][j] = max([m[i-1][j], m[i-1][j-items[i][0]] + items[i][1]])

	for i in m:
		for j in i:
			print("%d\t" % j, end="")
		print("")

	ret = []
	i = len(items)-1
	j = ksize
	while i >= 0 and j >= 0:
		if m[i][j] != m[i-1][j]:
			ret.append(items[i])
			i -= 1
			j -= items[i][0]
		else:
			i -= 1

	return m[len(items)-1][ksize], ret


def knapsack_own(ksize, items):
	pass


def parse_input(filename):
	"""Parse input data; returns the number of items in the knapsack first, and a list of items second. In the items
	array of tuples(-ish, they're n=2 lists), weight is first, value is second"""
	with open(filename, 'r') as file:
		data = file.read().split('\n')
		ksize = int(data[0])
		kweights = data[1].split(",")
		kvalues = data[2].split(",")
		kitems = []
		for i in range(0, len(kweights)):
			kitems.append([int(kweights[i]), int(kvalues[i])])
		return ksize, kitems


if len(sys.argv) != 2:
	print("Invalid number of arguments")
	exit(132)

ksize, items = parse_input(sys.argv[1])
rVal, rLst = knapsack_exhaustive(ksize, items)
print("Exhaustive result:\t%d\t%s" % (rVal, str(rLst)))
rVal, rLst = knapsack_dp(ksize, items)
print("Dynamic result:\t\t%d\t%s" % (rVal, str(rLst)))

