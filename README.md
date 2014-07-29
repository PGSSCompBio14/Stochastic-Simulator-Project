Stochastic-Simulator-Project
============================
(DELETE EVERYTHING IN THE "()" )


Sample input file:

INITIALIZATION:

	i = 500   (Number of iterations)
	t = 20    (duration time)
	of = 1    (Output frequency)
END

MOLECULES:
			(initial number of each "molecule")
	A = 2123
	B = 1
	C = 50
END

REACTIONS:

	A + 2B -> C [1.25]    (reaction with reaction rate)
	2C + 3B -> 3A [2.5]

END

OUTPUT:
			(name of output files)
	A = "A.txt"
	B = "B.txt"
	C = "C.txt"
	Plot = true




