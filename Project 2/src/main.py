import json

#def closestPairBruteForce(coords):
#    """Accepts a list of coordinates in array form. Finds the closest
#    pair of coordinates. Isn't very efficient about it."""


#def closestPairRecursive(coords):


def parseInputFile(filename):
    """Parses an input file in the form of [(X1,Y1),(X2,Y2),(X3,Y3),...(XN,YN)],
    returning it as an Nx2 array. This is accomplished by reading the whole thing
    in, replacing parens with square brackets, and... using the python json parser
    on the result. I'm so sorry."""
    with open(filename, "r") as file:
        data = file.read().replace("(", "[").replace(")", "]")
    return json.loads(data)

print(parseInputFile("input.txt")[0])
