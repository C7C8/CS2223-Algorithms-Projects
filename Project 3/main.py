import sys


def knapsack_exhaustive(ksize, items):
	pass


def knapsack_dp(ksize, items):
	pass


def knapsack_own(kszie, items):
	pass


def parse_input(filename):
	"""Parse input data; returns the number of items in the knapsack first, and a list of items second"""
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

ksize,items = parse_input(sys.argv[1])