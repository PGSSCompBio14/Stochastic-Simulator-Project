Stochastic-Simulator-Project
============================

Sample input file:

INITIALIZATION:

	i = 500
	t = 20
	of = 1
END

MOLECULES:

	A = 2123
	B = 1
	C = 50
END

REACTIONS:

	A + 2B -> C [1.25]
	2C + 3B -> 3A [2.5]

END

OUTPUT:

	A = "A.txt"
	B = "B.txt"
	C = "C.txt"
	Pot = true




