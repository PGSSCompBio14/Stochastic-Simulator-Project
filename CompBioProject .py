import random as rng
import math

def computeProp(molecules, k, reactions): #Finds the propensity of each reaction ocurring, returns a list of the propensities
    props = []
    i = 0
    cVal = 0
    for reaction in reactions: #goes through and computes the propensity for each reaction
            cVal= k[i]
            for key in reaction[0]:
                    if reaction[0][key] < 0:
                            cVal = cVal * molecules[key]
                    if (molecules[key] + reaction[0][key]) < 0:
                            cVal = 0
            props.append(cVal)
            i= i+1
    return props
                            
def reactUpdater(molecules, reaction):
    for sideOfReaction in reaction: #molecule = key in dictionary
            for molecule in sideOfReaction:
                molecules[molecule] += sideOfReaction[molecule]
           

def open_output_files(objects):
    files= {}
    
    for molecule in objects: #thing = (ex. "A", "B", "C"), types = molecules 
            
            files[molecule] =open(molecule + ".txt", "w") #in future, possibly add conditions

    return (files)

def write_data_to_output(outs, timer, molecules):
    for mol in molecules:
            outs[mol].write("%5.4e  %d\n" %(timer, molecules[mol]))

def close_output_files(outputs):
    for ou in outputs:
            outputs[ou].close()

def initEdit(strippedLine):
    if "i" in strippedLine:
            global maxIter
            maxIter = int(strippedLine.strip(" i="))
                    
    else: 
            if "t" in strippedLine:
                    global maxTime
                    maxTime = int(strippedLine.strip(" t="))
                    

def moleculesEdit(strippedLine):
    list = strippedLine.split("=")
    molecules[list[0].strip()] = int(list[1])


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
    
def parse():
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
                        maxIter = initEdit(strippedLine)
                    if blockCount == 2:
                        moleculesEdit(strippedLine)
                    if blockCount == 3:
                        reactionsEdit(strippedLine)

def main():
    parse()
    
    rng.seed(124213)
    time = 0.0
    iter = 0
    outputFreq = 1
    totalProps = 1
    
    filesdict = open_output_files(molecules)
    
    while ((time < maxTime) & (iter < maxIter)):
            propensities = computeProp(molecules, ka, reactions)
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

                reactUpdater(molecules, reactions[count-1])
            if(iter % outputFreq == 0):
                    write_data_to_output(filesdict, time, molecules)
                    
            iter += 1

            
    close_output_files(filesdict)


    
maxIter = 0
maxTime = 0
molecules = {}
ka = []
reactions = []

main()


