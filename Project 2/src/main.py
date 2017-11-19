#!/usr/bin/python3
from math import sqrt
from sys import argv
from timeit import timeit
import json


def parseInput(data):
	"""Parses an input string in the form of [(X1,Y1),(X2,Y2),(X3,Y3),...(XN,YN)],
	returning it as an Nx2 array. This is accomplished by replacing parens with
	square brackets, and... using the python json parser on the result. I'm so sorry."""
	return json.loads(data.replace("(", "[").replace(")", "]"))


def distance(c1, c2):
	"""Get distance between two points"""
	return sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[0]) ** 2)


def CP_BruteForce(coords):
	"""Accepts a list of coordinates in array form. Finds the closest
	pair of coordinates, returning the distance between them. Not very
	efficient about anything I don't recommend using this thing."""
	minDistance = 999999999.9
	for c1 in coords:
		for c2 in coords:
			if c1 == c2:
				continue
			d = distance(c1, c2)
			if d < minDistance:
				minDistance = d
	return minDistance


def CP_Recursive(coords):
	"""Works some recursive magic to find the smallest distance between two
	of the coordinates in the provided set. This function should be used as
	the entry point into the *actual* recursive algorithm (below), as it has
	to sort the coordinate list two different ways first.

	Realistically, this is just a cheap trick to make the timing code easier."""
	return CP_RecurseWorker(sorted(coords, key=lambda c: c[0]), sorted(coords, key=lambda c: c[1]))


def CP_RecurseWorker(P, Q):
	"""Performs the actual recursion work, since a little setup is needed
	prior to using this thing."""
	size = len(P)
	if size <= 3:
		return CP_BruteForce(P)

	Pl = P[0:int(size/2)]  # I LOVE THIS LANGUAGE
	Ql = P[0:int(size/2)]
	Pr = P[int(size/2):]
	Qr = P[int(size/2):]
	dl = CP_RecurseWorker(Pl, Ql)
	dr = CP_RecurseWorker(Pr, Qr)
	d = dl if dl < dr else dr
	m = P[int(size/2)-1][0]
	S = list(filter(lambda x: abs(x[0] - m) < d, Q))  # RACKET IS CALLING TO ME
	dminsq = d**2
	for i in range(0, len(S) - 2):
		k = i + 1
		while k <= len(S) - 1 and (S[k][1] - S[i][1])**2 < dminsq:
			temp = (S[k][0] - S[i][0])**2 + (S[k][1] - S[i][1])**2
			dminsq = temp if temp < dminsq else dminsq
			k += 1

	return sqrt(dminsq)


def CPWrapper(algo, coords):
	"""Wrapper so that we can pass data to a function that the timeit library will call"""
	def wrapped():
		return algo(coords)
	return wrapped


if len(argv) != 2:
	coordstr = str(input("Input list of coordinates in [(X1, Y1),(X2,Y2),...(XN,YN)] form:\n"))
else:
	with open(argv[1], "r") as inputFile:
		coordstr = inputFile.read()

print(CP_Recursive(parseInput(coordstr)))
