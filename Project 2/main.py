#!/usr/bin/python3
from math import sqrt
from sys import argv
from timeit import timeit
from json import JSONDecodeError
from random import randint
from optparse import OptionParser
import json


def parseInput(data):
	"""Parses an input string in the form of [(X1,Y1),(X2,Y2),(X3,Y3),...(XN,YN)],
	returning it as an Nx2 array. This is accomplished by replacing parens with
	square brackets, and... using the python json parser on the result. I'm so sorry.

	The return form is a 3D array because multiple data sets can be contained within
	one input string."""
	data = data.replace("(", "[").replace(")", "]")
	try:
		return [json.loads(data)]
	except JSONDecodeError:
		if data.endswith("\n"):
			data = data[0:len(data)-1]
		data = "[" + data.replace("\n", ",") + "]"   # Should allow multiple lines of JSON input
		return json.loads(data)



def distance(c1, c2):
	"""Get distance between two points"""
	return sqrt(((c1[0] - c2[0]) ** 2) + ((c1[1] - c2[1]) ** 2))


def CP_BruteForce(coords):
	"""Accepts a list of coordinates in array form. Finds the closest
	pair of coordinates, returning the distance between them. Not very
	efficient about anything I don't recommend using this thing."""
	minDistance = 999999999.9
	for c1 in coords:
		for c2 in coords[coords.index(c1)+1:]:
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


# Process command line options
parser = OptionParser()
parser.add_option("-c", "--csv", dest="csv", action="store_true", default=False,
					help="enable machine-readable CSV output")
parser.add_option("-r", "--random", dest="random", action="store_true", default=False,
					help="use random coordinate sets instead of user input")
parser.add_option("-f", "--file", dest="filename", action="store", type="string",
					help="load coordinate sets from possibly multiline file")
(options, args) = parser.parse_args()


# Obtain coordinate sets; the user may be pestered for input if no file is provided and random is not set
if options.random:
	temp = []
	for size in range(5, 256):
		current = []
		for i in range(0, size):
			current.append([randint(0, 100), randint(0, 100)])
		temp.append(current)

	# Strip off the first and last bracket so the parser function recognizes it as a multi set input. Yes, this is
	# hideous. Yes, this sort of code keeps me up at night. Sorry for sharing this horror with you, grader...
	coordstr = json.dumps(temp)[1:-1]

elif options.filename is None:
	coordstr = str(input("Input list of coordinates in [(X1, Y1),(X2,Y2),...(XN,YN)] form:\n"))
	if len(coordstr) == 0:
		print("Didn't receive any user input, exiting!")
		exit(1)
else:
	with open(options.filename, "r") as inputFile:
		coordstr = inputFile.read()
coordSets = parseInput(coordstr)

# Run trials, human readable
if not options.csv:
	if len(coordSets) > 1:
		print("Processing %d sets of coordinates..." % len(coordSets))
	for coords in coordSets:
		print("Finding minimum distance in set(%d): %s" % (len(coords), str(coords)))
		print("Brute force:\t%f (%f s)" % (CP_BruteForce(coords), timeit(CPWrapper(CP_BruteForce, coords), number=100)))
		print("Recursive:\t\t%f (%f s)\n" % (CP_Recursive(coords), timeit(CPWrapper(CP_Recursive, coords), number=100)))
else:
	# Run trials, but with CSV output
	print("Size,Value,BruteForce,Recursive,Set")
	for coords in coordSets:
		print("%d,%f,%f,%f,%s" % (len(coords),  CP_Recursive(coords),
							timeit(CPWrapper(CP_BruteForce, coords), number=100),
							timeit(CPWrapper(CP_Recursive, coords), number=100),
							str(coords).replace(",", ";")))
