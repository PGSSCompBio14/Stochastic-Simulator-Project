Stochastic-Simulator-Project
============================
(DELETE EVERYTHING IN THE "()" )


Sample input file:

INITIALIZATION:

	i = 500   (maximum number of iterations)
	t = 20    (duration time)
	of = 1    (output frequency)
END

MOLECULES:
			
	A = 2123	(initial number of each "molecule")
	B = 1
	C = 50
END

REACTIONS:

	A + 2B -> C [1.25]    (reaction with reaction rate)
	2C + 3B -> 3A [2.5]
END

OUTPUT:

	A = "A.txt"  (names of output files)
	B = "B.txt"
	C = "C.txt"
	Plot = true
	A vs. C      (which molecules will be graphed)
END



