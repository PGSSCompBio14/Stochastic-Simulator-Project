#!/usr/bin/env python

maxIterations = 0
maxTime = 0
molDict = {}
ka = []
reactions = []

def initEdit(strippedLine):
	if "i" in strippedLine:
		maxIterations = int(strippedLine.strip(" i="))
			
	else: 
		if "t" in strippedLine:
			maxTime = int(strippedLine.strip(" t="))
			

def moleculesEdit(strippedLine):
	list = strippedLine.split("=")
	molDict[list[0].strip()] = int(list[1])


def reactionsEdit(strippedLine):
    
    rxnDict = {}
    
    initialSplit = strippedLine.split("[")	

    reactionArray = initialSplit[0].split("->")
    reactants = reactionArray[0]
    products = reactionArray[1]
    reactantsFinal = reactants.split("+")
    productsFinal = products.split("+")
    
    print initialSplit
    kavalue = initialSplit[1].strip(" ]")
    ka.append(float(kavalue))	
    print ka

    for reac in reactantsFinal:
        reactant = reac.strip()
	count = 0
        for digit in reactant:
            if digit.isdigit():
                count+=1 
            else:
                if count == 0:
                    rxnDict[reactant[count:]] = -1
                else:
                    rxnDict[reactant[count:]] = -1*int(reactant[0:count])

    for prod in productsFinal:
	product = prod.strip()
        count = 0
        for digit in product:
            if digit.isdigit():
                count+=1   
            else:
                if count == 0:
                    rxnDict[product[count:]] = 1
                else:
                    rxnDict[product[count:]] = 1*int(product[0:count])
    reactions.append(rxnDict)
	
def main():
	file = open("parse.txt")

	blockCount = 0

	for line in file.readlines():
		strippedLine = line.strip()
		if strippedLine != "":
			if blockCount == 0:
				if strippedLine == "INITIALIZATION:":
					blockCount = 1
				if strippedLine == "MOLECULES:":
					blockCount = 2
				if strippedLine == "REACTIONS:":
					blockCount = 3
			else:
				if strippedLine == "END":
					blockCount = 0
				else:
					if blockCount == 1:
						initEdit(strippedLine)
					if blockCount == 2:
						moleculesEdit(strippedLine)
					if blockCount == 3:
						reactionsEdit(strippedLine)
	print reactions


if __name__ == "__main__":
    main()