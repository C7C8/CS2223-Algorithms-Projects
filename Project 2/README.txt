To run:

./main.py [-rft] [-c]

Options:
	-r: Random mode, generate a series of point sets to test on
	-f: File mode, read from an input file. Can be multi-line. See input.txt for example
	-t: Test mode, verifies that output from recursive algorithm matches the expected output.
	    Not compatible with CSV option.
	-c: Enable CSV output, see output.csv for example

If no flags are provided, the program will request input from the user. For more information, run with -h.

These point sets have been used to verify the algorithms; their output may be found in Report.pdf
[(0,1),(99,50),(153,22),(44,11)]
[(0, 0), (7, 6), (2, 20), (12, 5), (16, 16), (5, 8), (19, 7), (14, 22), (8, 19), (7, 29), (10, 11), (1, 13)]
[[14, 13], [88, 1], [13, 41], [83, 19], [9, 1], [86, 78], [98, 56], [19, 91], [21, 8], [79, 35]]


Note that THERE ARE NO effRec() OR effBF() FUNCTIONS; THE PYTHON TIMEIT LIBRARY WAS USED INSTEAD. You'll
find this eliminates need for manual timing. Timeit works by accepting a function (functions are first-class
objects in python) and returning a float that tells how long it took to run. Since you can use multiple trials
per function, I chose 100 trials.
