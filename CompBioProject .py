import matplotlib.pyplot as plt
import random as rng
import math
from copy import *
import sys


def plotOutput(times, currentMolecules, numberOfMolecules):
    """
    Creates and displays a graph in a new window of concentration versus time with lines of data points for each molecule
    """
    moleculeData = []
    for molecule in numberOfMolecules:
        moleculeData = []
        for integer in range(0, len(currentMolecules)):
            moleculeData.append(currentMolecules[integer][molecule])
        plt.plot(times, moleculeData, label = molecule)
    plt.xlabel('Time Elapsed (seconds)')
    plt.ylabel('Number of Molecules')
    plt.title('Number of Molecules Vs. Time')
    plt.legend()
    plt.show()

def computeProp(numberOfMolecules, k, reactions):
    """
    Finds the propensity of each reaction occurring, returns a list of the propensities
    """
    props = []
    i = 0
    currentPropensity = 0
    for reaction in reactions: #goes through and computes the propensity for each reaction
        reactants = reaction[0]
        currentPropensity= k[i]
        for reactant in reactants:
            for int in range(0, abs(reactants[reactant])):
                currentPropensity *= numberOfMolecules[reactant] - int
        props.append(currentPropensity)
        i = i+1
    return props

def reactUpdater(numberOfMolecules, reaction):
    """
    Subtracts the specified number of reactants and adds the products to the molecule amounts to represent a reaction
    being carried out.
    """
    for sideOfReaction in reaction:
            for molecule in sideOfReaction:
                numberOfMolecules[molecule] += sideOfReaction[molecule]


def open_output_files(outputMolecules): #Chooses files and prepares them to output to
    files = {}

    for key in outputMolecules:
            files[key] = open(outputMolecules[key], "w") #in future, possibly add conditions

    return files

def write_data_to_output(outs, timer, numberOfMolecules, outputMolecules): #Writes time and number of molecules to each of the files
    for molecule in outputMolecules:
            outs[molecule].write("%5.4e %d\n" %(timer, numberOfMolecules[molecule]))

def close_output_files(outputs): #Closes all output files
    for ou in outputs:
            outputs[ou].close()

def initEdit(strippedLine):
    if "i" in strippedLine:
        definedConditions["maxIter"] = int(strippedLine.strip(" i="))
    elif "t" in strippedLine:
        definedConditions["maxTime"] = float(strippedLine.strip(" t="))
    elif "of" in strippedLine:
        definedConditions["outputFrequency"] = int(strippedLine.strip(" of="))

def moleculesEdit(strippedLine):
    list = strippedLine.split("=")
    numberOfMolecules[list[0].strip()] = int(list[1])

def reactionsEdit(strippedLine):

    rxnDict = []
    reactantDict = {}
    productDict = {}

    initialSplit = strippedLine.split("[")
    if "=" in strippedLine:
        reactionArray = initialSplit[0].split("=")
    else:
        reactionArray = initialSplit[0].split("->")
    reactants = reactionArray[0]
    products = reactionArray[1]
    if "*" in reactants:
        reactantsFinal = reactants.split("*")
    else:
        reactantsFinal = reactants.split("+")
    if "*" in products:
        productsFinal = products.split("*")
    else:
        productsFinal = products.split("+")
    kavalue = initialSplit[1].strip(" ]")
    ka.append(float(kavalue))

    for reac in reactantsFinal:
            reactant = reac.strip()
            count = 0
            for digit in reactant:
                    if digit.isdigit():
                            count+=1
                    else:
                        if reactant[count:] not in numberOfMolecules:
                            print "Molecule used in one of the reactions that is not in molecule list"
                            sys.exit(1)
                        else:
                                if count == 0:
                                        reactantDict[reactant[count:]] = -1

                                else:
                                        reactantDict[reactant[count:]] = -1*int(reactant[0:count])

    for prod in productsFinal:
        product = prod.strip()
        count = 0
        for digit in product:
                if digit.isdigit():
                        count+=1
                else:
                        if count == 0:
                                productDict[product[count:]] = 1
                        else:
                                productDict[product[count:]] = 1*int(product[0:count])
    rxnDict.append(reactantDict)
    rxnDict.append(productDict)
    reactions.append(rxnDict)


def outputEdit(strippedLine):
    if "\"" in strippedLine:
        initialSplit = strippedLine.split("=")
        moleculeName = initialSplit[0].strip()
        outputFileName = initialSplit[1].strip(" \"")
        outputMolecules[moleculeName] = outputFileName
    else:
        initialSplit = strippedLine.split("=")
        plotString = initialSplit[1].strip()
        if plotString.upper().startswith("T"):
            definedConditions["Plot"] = True
        else:
            definedConditions["Plot"] = False

def Getinput():
    File = input("What is the file name? Use quotes around the File name: " )## specifies a file to use

def parse(): ## goes through text file and establishes initial conditions
    file = open(GetInput())
    blockCount = 0 ## keeps track of which section of the file is being parsed
    for line in file.readlines():
        strippedLine = line.strip() ## deletes all white space before and after text
        if strippedLine != "":
            if blockCount == 0:
                if "INITIALIZATION" in strippedLine:
                    blockCount = 1
                if "MOLECULES" in strippedLine:
                    blockCount = 2
                if "REACTIONS" in strippedLine:
                    blockCount = 3
                if "OUTPUT" in strippedLine:
                    blockCount = 4
            else:
                if "END" in strippedLine:
                    blockCount = 0
                else:
                    if blockCount == 1:
                        initEdit(strippedLine)
                    if blockCount == 2:
                        moleculesEdit(strippedLine)
                    if blockCount == 3:
                        reactionsEdit(strippedLine)
                    if blockCount == 4:
                        outputEdit(strippedLine)

def main():
    parse()
    rng.seed(124213)
    time = 0.0
    iter = 0
    totalProps = 1
    times = []
    currentMolecules = []
    filesdict = open_output_files(outputMolecules)
    while ((time < definedConditions["maxTime"]) and (iter < definedConditions["maxIter"])):
            propensities = computeProp(numberOfMolecules, ka, reactions)
            totalProps = sum(propensities)
            if(totalProps != 0):
                rand1 = rng.random()

                tau = 1.0/totalProps*math.log(1/rand1)
                time += tau

                rand2 = rng.random()
                threshold = totalProps * rand2
                summation = propensities[0]
                count = 1

                while threshold > summation:
                        summation += propensities[count]
                        count +=1

                reactUpdater(numberOfMolecules, reactions[count - 1])

            if(iter % definedConditions["outputFrequency"] == 0): # Saves data point when output frequency is reached
                    write_data_to_output(filesdict, time, numberOfMolecules, outputMolecules)
                    times.append(time)
                    nOM = deepcopy(numberOfMolecules)
                    currentMolecules.append(nOM)


            iter += 1

    close_output_files(filesdict)
    plotOutput(times, currentMolecules, numberOfMolecules)



outputMolecules = {}
definedConditions = {}
numberOfMolecules = {}
ka = []
reactions = []

main()

