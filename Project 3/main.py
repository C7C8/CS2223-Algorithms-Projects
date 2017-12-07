import sys
from random import randint
from itertools import chain
from itertools import combinations
from timeit import timeit


def knapsack_exhaustive(ksize, items):
	"""Conduct exhaustive search by iterating over the power set of the input item list. This is absurdly expensive"""
	# Why do in a loop what you can do with a few lambdas?
	powerset = chain.from_iterable(combinations(items, r) for r in range(len(items)+1))
	powerset = filter(lambda s: sum(map(lambda i: i[0], s)) <= ksize, powerset)
	best = max(powerset, key=lambda s: sum(map(lambda i: i[1], s)))
	return sum(map(lambda i: i[1], best)), best


def knapsack_dp(ksize, items):
	"""Solve knapsack problem using dynamic programming."""
	table = [[0 for i in range(ksize+1)] for j in range(len(items))]
	for i in range(len(items)):
		for j in range(ksize+1):
			if items[i][0] > j:
				table[i][j] = table[i-1][j]
			else:
				table[i][j] = max([table[i-1][j], table[i-1][j-items[i][0]] + items[i][1]])

	ret = []
	i = len(items)-1
	j = ksize
	while i > 0 and j >= 0:
		if table[i][j] != table[i-1][j]:
			ret.append(items[i])
			j -= items[i][0]
			i -= 1
		else:
			i -= 1

	return table[len(items)-1][ksize], ret


def knapsack_own(ksize, items):
	"""Do some recursive magic stuff to try to find a solution. I can't guarantee that this will actually work..."""

	if len(items) <= 3:
		return knapsack_exhaustive(ksize, items)

	# Divide the list into two parts, sorted by weight. This is magic.
	items = sorted(items, key=lambda x: x[0])
	l = items[::2]
	r = items[1::2]
	lweight = sum(map(lambda i: i[0], l))
	rweight = sum(map(lambda i: i[0], r))
	lres, litems = knapsack_own((lweight / ksize) * ksize * 0.707, l)
	rres, ritems = knapsack_own((rweight / ksize) * ksize * 0.707, r)
	return knapsack_exhaustive(ksize, litems + ritems)


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


def genList(maxItems, maxWeight, maxValue):
	"""Generate a list of random items"""
	return [[randint(1, maxWeight), randint(1, maxValue)] for x in range(maxItems)]

def wrapper(algo, ksize, items):
	def wrapped():
		return algo(ksize, items)
	return wrapped

ksize = 0
items = []
if len(sys.argv) == 2:
	ksize, items = parse_input(sys.argv[1])
elif len(sys.argv) == 1:
	ksize = randint(1, 100)
	items = genList(10, 20, 100)
else:
	print("Invalid number of arguments")
	exit(132)

# print("Knapsack size:\t\t%d\t\t%s" % (ksize, str(items)))
# rVal, rLst = knapsack_exhaustive(ksize, items)
# rWgt = sum(map(lambda i: i[0], rLst))
# print("Exhaustive result:\t%d, %d\t%s" % (rVal, rWgt, str(rLst)))
# rVal, rLst = knapsack_dp(ksize, items)
# rWgt = sum(map(lambda i: i[0], rLst))
# print("Dynamic result:\t\t%d, %d\t%s" % (rVal, rWgt, str(rLst)))
# rVal, rLst = knapsack_own(ksize, items)
# rWgt = sum(map(lambda i: i[0], rLst))
# print("Own result:\t\t\t%d, %d\t%s" % (rVal, rWgt, str(rLst)))

out = [["Dynamic", "Own"]]
# Range of items to test for...
for itemcount in range(3, 23):
	# Number of trials...
	print("Testing on %d items..." % itemcount)
	line = [0, 0]
	for trial in range(100):
		ksize = randint(20, 100)
		items = genList(itemcount, 20, 100)
		line[0] += timeit(wrapper(knapsack_dp, ksize, items), number=5)
		line[1] += timeit(wrapper(knapsack_own, ksize, items), number=5)
	line[0] /= 100.0
	line[1] /= 100.0
	out.append(line)

with open("output.csv", "w+") as file:
	for line in out:
		file.write("%s, %s\n" % (line[0], line[1]))
