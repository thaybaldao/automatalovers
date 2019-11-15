import math as m
import random as r

def generateCromossomes(numGenes, numPopulation):
    popul = []
    for i in range(0, numPopulation):
        crom = []
        for j in range(0, numGenes):
            crom.append(r.randint(1,256))
        popul.append(crom)

    return popul

def updateGrammar(term, j, k):
    if grammar[j] == term:
        grammar[j+1:j+1] = rules[term][popul[0][k]%len(rules[term])]
        del grammar[j]

numGenes = 6
numPopulation = 4
popul = generateCromossomes(numGenes, numPopulation)


rules = {"e": [["e", "o", "e"], ["v"]],
         "o": ["+", "-", "/", "*"],
         "v": ["x", "y"]}

grammar = ["e"]

updateGrammar("e", 0, 0)
print(grammar)
