#!/usr/bin/python3
from math import sqrt
from sys import argv
import json


def parseInput(data):
	"""Parses an input string in the form of [(X1,Y1),(X2,Y2),(X3,Y3),...(XN,YN)],
	returning it as an Nx2 array. This is accomplished by replacing parens with
	square brackets, and... using the python json parser on the result. I'm so sorry."""
	data = data.replace("(", "[").replace(")", "]")
	return json.loads(data)


def distance(c1, c2):
	"""Get distance between two points"""
	return sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[0]) ** 2)


def closestPairBruteForce(coords):
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


def closestPairRecursive(coords):
	"""Accepts a list of coordinates in array form. Works some recursive magic
	to find the closest pair of coordinates in a way that is... faster? Anyways,
	this too returns the smallest distance."""


if len(argv) != 2:
	coordstr = str(input("Input list of coordinates in [(X1, Y1),(X2,Y2),...(XN,YN)] form:\n"))
else:
	with open(argv[1], "r") as inputFile:
		coordstr = inputFile.read()

print(closestPairBruteForce(parseInput(coordstr)))
