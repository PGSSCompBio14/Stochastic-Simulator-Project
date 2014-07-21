import random as rng
import math

def computeProp(numberOfMolecules, k, reactions): #finds the propensity of each reaction, returns a list of the propensities
    props = []
    i = 0
    currentPropensity = 0
    for reaction in reactions: 
            currentPropensity= k[i]
            for key in reaction[0]:
                for int in range(0, abs(reaction[0][key])): #if there are not enough reactant molecules, propensity set to zero
                    currentPropensity *= numberOfMolecules[key] - int 
            props.append(currentPropensity) 
            i = i+1
    return props
                            
def reactUpdater(numberOfMolecules, reaction): # Carries out given reaction
    for sideOfReaction in reaction: 
            for molecule in sideOfReaction:
                numberOfMolecules[molecule] += sideOfReaction[molecule]
           

def open_output_files(outputMolecules): ##Creates and opens output files for specified molecules
    files = {}
    
    for key in outputMolecules:  
            files[key] = open(outputMolecules[key], "w") 

    return files

def write_data_to_output(outs, timer, numberOfMolecules, outputMolecules): #Updates data files with current time and number of molecules
    for molecule in outputMolecules:
            outs[molecule].write("%5.4e  %d\n" %(timer, numberOfMolecules[molecule]))

def close_output_files(outputs): #Closes all output files
    for ou in outputs:
            outputs[ou].close()


#parses the initialization section of the input file
#stores values for maximum time, maximum iterations, and output frequency in the definedConditions dictionary
def initEdit(strippedLine): 
    if "i" in strippedLine:
        definedConditions["maxIter"] = int(strippedLine.strip(" i="))
    elif "t" in strippedLine:
        definedConditions["maxTime"] = int(strippedLine.strip(" t="))
    elif "of" in strippedLine:
        definedConditions["outputFrequency"] = int(strippedLine.strip(" of="))

#parses the molecules section of the input file
#stores the initial number of each molecule in the numberOfMolecules dictionary
def moleculesEdit(strippedLine):
    list = strippedLine.split("=")
    numberOfMolecules[list[0].strip()] = int(list[1])

#parses the reactions section of the input file
#stores each reaction into the reactions list
#within each reaction, there is a reactants and products dictionary
#the key for each molecule is its name and the value is the number of molecules that are added or subtracted 
    #each time the reaction is carried out
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
   
#parses the output section of the input file
#determines which molecules are to be plotted and stores the user's desired names for the ouput files
#adds a variable with key "Plot" to the definedConditions dictionary whose value (boolean) determines whether or not a graph will be plotted 
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
    
def parse(): ## goes through text file and establishes initial conditions
    file = open("parse.txt")
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
    
    filesdict = open_output_files(outputMolecules)
    
    while ((time < definedConditions["maxTime"]) & (iter < definedConditions["maxIter"])):
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
            
            if(iter % definedConditions["outputFrequency"] == 0):
                    write_data_to_output(filesdict, time, numberOfMolecules, outputMolecules)
                    
            iter += 1
            
    close_output_files(filesdict)



outputMolecules = {}
definedConditions = {}   
numberOfMolecules = {}
ka = []
reactions = []

main()


