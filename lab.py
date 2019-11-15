import math as m
import random as r
# Definir o numero de genes: 25
# Definir o tamanho da populacao:16
# Definir a probabilidade de cruzamento: 0.8
# Definir a probabilidade de mutacao: 0.1

def generateCromossomes(numGenes, numPopulation):
    popul = []
    for i in range(0, numPopulation):
        crom = []
        for j in range(0, numGenes):
            crom.append(r.randint(1,256))
        popul.append(crom)

    return popul

def updateGrammar(term, j, k):
    print('update')
    if grammar[j] == term:
        grammar[j+1:j+1] = rules[term][crom[k]%len(rules[term])]
        del grammar[j]

def verifyEnd(grammar):
    end = True
    for i in range(0, len(grammar)):
        if grammar[i] == "e" or grammar[i] == "o" or grammar[i] == "v":
            end = False
            break

    return end

numGenes = 6
numPopulation = 4
popul = generateCromossomes(numGenes, numPopulation)

rules = {"e": [["e", "o", "e"], ["v"]],
         "o": ["+", "-", "/", "*"],
         "v": ["x", "y"]}

grammarList = []
for i in range(0, len(popul)):
    crom = popul[i]
    grammar = ["e"]

    p = 0
    while not verifyEnd(grammar) and p < 3:
        for k in range(0, len(crom)):
            j = 0
            while j <len(grammar):
                if grammar[j] == "e" or grammar[j] == "o" or grammar[j] == "v":
                    break
                j += 1

            if j == len(grammar):
                break
            else:
                if grammar[j] == "e":
                    updateGrammar("e", j, k)
                elif grammar[j] == "o":
                    updateGrammar("o", j, k)
                elif grammar[j] == "v":
                    updateGrammar("v", j, k)
        p +=1

    grammarList.append(grammar)
print(grammarList)
