import math as m
import random as r
import pandas as pd

#varNames = ["ID","Cement","Blasr", "FlyAsh", "Water", "Superplasticizer", "CoarseAggregate", "FineAggregate","Age","strength"]
#varNames = ["ID","x1","x2","x3","x4","x5","x6","x7","x8","strength"]
dataTraining = pd.read_csv("training.csv")
ID = dataTraining["ID"].tolist()

x1 = dataTraining["Cement"].tolist()
x2 = dataTraining["Blasr"].tolist()
x3 = dataTraining["FlyAsh"].tolist()
x4 = dataTraining["Water"].tolist()
x5 = dataTraining["Superplasticizer"].tolist()
x6 = dataTraining["CoarseAggregate"].tolist()
x7 = dataTraining["FineAggregate"].tolist()
x8 = dataTraining["Age"].tolist()

strength = dataTraining["strength"].tolist()
print(x1)

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

#comando para formar string a partir da lista de terminais: string = ''.join([str(elem) for elem in v1])
# em seguida fazer eval(string)  :)
