import random as rng
import math

def computeProp(numberOfMolecules, k, reactions): #Finds the propensity of each reaction occurring, returns a list of the propensities
    props = []
    i = 0
    currentPropensity = 0
    for reaction in reactions: #goes through and computes the propensity for each reaction
            currentPropensity= k[i]
            for key in reaction[0]:
                    if reaction[0][key] < 0:
                            currentPropensity = currentPropensity * numberOfMolecules[key]
                    if (numberOfMolecules[key] + reaction[0][key]) < 0:
                            currentPropensity = 0
            props.append(currentPropensity) 
            i = i+1
    return props
                            
def reactUpdater(numberOfMolecules, reaction): # Carries out given reaction
    for sideOfReaction in reaction: 
            for molecule in sideOfReaction:
                numberOfMolecules[molecule] += sideOfReaction[molecule]
           

def open_output_files(objects): #Chooses files and prepares them to output to
    files= {}
    
    for molecule in objects:  
            files[molecule] = open(molecule + ".txt", "w") #in future, possibly add conditions

    return (files)

def write_data_to_output(outs, timer, numberOfMolecules): #Writes time and number of molecules to each of the files
    for mol in numberOfMolecules:
            outs[mol].write("%5.4e  %d\n" %(timer, numberOfMolecules[mol]))

def close_output_files(outputs): #Closes all output files
    for ou in outputs:
            outputs[ou].close()

def initEdit(strippedLine):
    if "i" in strippedLine:
        definedConditions["maxIter"] = int(strippedLine.strip(" i="))
    elif "t" in strippedLine:
        definedConditions["maxTime"] = int(strippedLine.strip(" t="))
    elif "of" in strippedLine:
        defineConditions["outputFrequency"] = int(strippedLine.strip(" of="))

def moleculesEdit(strippedLine):
    list = strippedLine.split("=")
    numberOfMolecules[list[0].strip()] = int(list[1])

def reactionsEdit(strippedLine):
    
    rxnDict = []
    reactantDict = {}
    productDict = {}
    
    initialSplit = strippedLine.split("[")	

    reactionArray = initialSplit[0].split("->")
    reactants = reactionArray[0]
    products = reactionArray[1]
    reactantsFinal = reactants.split("+")
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
    
def parse(): ## goes through text file and establishes initial conditions
    file = open("parse.txt")
    blockCount = 0 ## keeps track of which section of the file is being parsed
    for line in file.readlines():
        strippedLine = line.strip() ## deletes all white space before and after text
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

def main():
    parse()
    rng.seed(124213)
    time = 0.0
    iter = 0
    totalProps = 1
    
    filesdict = open_output_files(numberOfMolecules)
    
    while ((time < maxTime) & (iter < maxIter)):
            propensities = computeProp(numberOfMolecules, ka, reactions)
            totalProps = sum(propensities)
            if(totalProps != 0):
                rand1 = rng.random()
                
                tau = 1.0/totalProps*math.log(1/rand1)
                time += tau
                rand2 = rng.random()
                threshold = totalProps * rand2
                summation = 0
                count = 0

                while threshold > summation:
                        summation += propensities[count]
                        count +=1

                reactUpdater(numberOfMolecules, reactions[count - 1])
            
            if(iter % definedConditions["outputFrequency"] == 0):
                    write_data_to_output(filesdict, time, numberOfMolecules)
                    
            iter += 1
            
    close_output_files(filesdict)


definedConditions = {"maxIter", "maxTime", "outputFrequency"}   
numberOfMolecules = {}
ka = []
reactions = []

main()


