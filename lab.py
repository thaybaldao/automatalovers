import math as m
import random as r
import pandas as pd
import numpy as np

# Definir o numero de genes: 25
# Definir o tamanho da populacao:16
# Definir a probabilidade de cruzamento: 0.8
# Definir a probabilidade de mutacao: 0.1

### Importar dados de treinamento
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

x_data = [0.9, 0.3, 0.5, 0.88, 0.6]
y_data = [0.8, 0.1, 0.2, 0.5, 0.7]
desired = [1.61, 0.19, 0.45, 1.2744, 1.06]

### Set-up
rules = {"e": [["e", "o", "e"], ["v"]],
         "o": ["+", "-", "/", "*"],
         "v": ["x", "y"]}


### Funcoes
def generateCromossomes(numGenes, numPopulation):
    popul = []
    for i in range(0, numPopulation):
        crom = []
        for j in range(0, numGenes):
            crom.append(r.randint(1,256))
        popul.append(crom)
    return popul

def updateGrammar(term, j, k, grammar, crom):
    if grammar[j] == term:
        grammar[j+1:j+1] = rules[term][crom[k]%len(rules[term])]
        del grammar[j]
    return grammar

def verifyEnd(grammar):
    end = True
    for i in range(0, len(grammar)):
        if grammar[i] == "e" or grammar[i] == "o" or grammar[i] == "v":
            end = False
            break
    return end

def convertGrammar(grammarList):
    grammarStringList = []
    for i in range(0, len(grammarList)):
        grammarStringList.append(''.join([str(elem) for elem in grammarList[i]]))
    return grammarStringList

def avaliateGrammar(grammarList):
    grammarStringList = convertGrammar(grammarList)
    mse = []
    for i in range(0, len(grammarStringList)):
        if not verifyEnd(grammarList[i]):
            mse.append(1000000)
        else:
            produced = []
            for j in range(0, len(x_data)):
                x = x_data[j]
                y = y_data[j]
                produced.append(eval(grammarStringList[i]))
            mse.append(np.square(np.subtract(produced, desired)).mean())
    # print("before", mse)
    min = 1000000
    max = -1
    for i in range(0, len(mse)):
        if mse[i] < min:
            min = mse[i]
        if (mse[i] is not 1000000) and (mse[i] > max):
            max = mse[i]

    for i in range(0, len(mse)):
        if mse[i] is not 1000000:
            if max != min:
                mse[i] = (mse[i] - min)/(max - min)
            else:
                mse[i] = 0
    # print("min", min, "max", max, "after", mse)
    return mse

def tournament(mse):
    winners = []
    for i in mse:
        player1 = r.randint(0, len(mse)-1)
        player2 = r.randint(0, len(mse)-1)

        if mse[player1] <= mse[player2]:
            winners.append(player1)
        else:
            winners.append(player2)
    return winners

def crossing(popul, winners, crossingProbability):
    nextPopul = []
    for i in range(0, len(winners), 2):
        number = r.random()
        if number < crossingProbability:
            crossingPosition = r.randint(1, len(popul[i]) - 1)
            son1 = popul[winners[i]][0:crossingPosition] + popul[winners[i+1]][crossingPosition:len(popul[i])]
            son2 = popul[winners[i+1]][0:crossingPosition] + popul[winners[i]][crossingPosition:len(popul[i])]
            nextPopul.append(son1)
            nextPopul.append(son2)
        else:
            nextPopul.append(popul[winners[i]])
            nextPopul.append(popul[winners[i+1]])
    return nextPopul

def mutation(popul, mutationProbability):
    for i in range(0, len(popul)):
        chooseMutation = []
        for j in range(0, len(popul[i])):
            chooseMutation.append(r.random())

        for j in range(0, len(popul[i])):
            if chooseMutation[j] < mutationProbability:
                popul[i][j] = r.randint(1,256)

    return popul

def grammarGenerator(popul, numGrammarFormation):
    grammarList = []
    for i in range(0, len(popul)):
        crom = popul[i]
        grammar = ["e"]
        p = 0
        while not verifyEnd(grammar) and p < numGrammarFormation:
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
                        grammar = updateGrammar("e", j, k, grammar, crom)
                    elif grammar[j] == "o":
                        grammar = updateGrammar("o", j, k, grammar, crom)
                    elif grammar[j] == "v":
                        grammar = updateGrammar("v", j, k, grammar, crom)
            p +=1

        grammarList.append(grammar)
    return grammarList

def chooseBestIndividual(popul, numGrammarFormation):
    grammarList = grammarGenerator(popul, numGrammarFormation)
    print(grammarList)
    mse = avaliateGrammar(grammarList)
    print(mse)
    bestCrom = grammarList[mse.index(min(mse))]
    return ''.join([str(elem) for elem in bestCrom])

def run(numIterations, mutationProbability, crossingProbability, numGenes, numPopulation, numGrammarFormation):
    popul = generateCromossomes(numGenes, numPopulation)
    for i in range(0, numIterations):
        grammarList = grammarGenerator(popul, numGrammarFormation)
        # print(grammarList)
        mse = avaliateGrammar(grammarList)
        # print(mse)
        winners = tournament(mse)
        # print(winners)
        # print(popul)
        popul = crossing(popul, winners, crossingProbability)
        # print(popul)
        popul = mutation(popul, mutationProbability)
        # print(popul)

    bestExp = chooseBestIndividual(popul, numGrammarFormation)
    print(bestExp)


run(100000, 0.1, 0.9, 6, 4, 15)
