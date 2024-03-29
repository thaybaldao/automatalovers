import math as m
import random as r
import pandas as pd
import numpy as np
import csv

### Importar dados de treinamento
dataTraining = pd.read_csv("training.csv")
ID = dataTraining["ID"].tolist()
x1Data = dataTraining["Cement"].tolist()
x2Data = dataTraining["Blasr"].tolist()
x3Data = dataTraining["FlyAsh"].tolist()
x4Data = dataTraining["Water"].tolist()
x5Data = dataTraining["Superplasticizer"].tolist()
x6Data = dataTraining["CoarseAggregate"].tolist()
x7Data= dataTraining["FineAggregate"].tolist()
x8Data = dataTraining["Age"].tolist()
strengthData = dataTraining["strength"].tolist()

### Set-up
rules = {"e": [["e", "a", "e"], ["(", "e", "a", "e", ")"], ["p", "(", "e", ")"], ["v"]],
         "a": ["+", "-", "/", "*"],
         "p": ["m.cos", "m.sin", "m.log", "m.sqrt"],
         "v": ["x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8"]}

### Funcoes
def generatePopulation(numGenes, numPopulation):
    popul = []
    for i in range(0, numPopulation):
        crom = []
        for j in range(0, numGenes):
            crom.append(r.randint(1,256))
        popul.append(crom)
    return popul

def updateExpression(expr, term, j, k, crom):
    if not (len(expr) == 1 and term == "e"):
        index = crom[k]%len(rules[term])
    else:
        index = crom[k]%(len(rules[term]) - 1)

    expr[j+1:j+1] = rules[term][index]
    del expr[j]
    return expr

def verifyEnd(expr):
    end = True
    for i in range(0, len(expr)):
        if expr[i] == "e" or expr[i] == "p" or expr[i] == "a" or expr[i] == "v":
            end = False
            break
    return end

def convertExpression(expressionsList):
    expressionStringList = []
    for i in range(0, len(expressionsList)):
        expressionStringList.append(''.join([str(elem) for elem in expressionsList[i]]))
    return expressionStringList

def avaliateExpressions(expressionsList):
    expressionStringList = convertExpression(expressionsList)
    mse = []
    for i in range(0, len(expressionStringList)):
        if not verifyEnd(expressionsList[i]):
            mse.append(1000000)
        else:
            produced = []
            for j in range(0, len(x1Data)):
                x1 = x1Data[j]
                x2 = x2Data[j]
                x3 = x3Data[j]
                x4 = x4Data[j]
                x5 = x5Data[j]
                x6 = x6Data[j]
                x7 = x7Data[j]
                x8 = x8Data[j]
                try:
                    evaluatingData = eval(expressionStringList[i])
                except:
                    evaluatingData = 1000000
                produced.append(evaluatingData)
            mse.append(np.square(np.subtract(produced, strengthData)).mean())
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
    return mse

def computeErrorWithoutNormalize(bestExp):
    produced = []
    for j in range(0, len(x1Data)):
        x1 = x1Data[j]
        x2 = x2Data[j]
        x3 = x3Data[j]
        x4 = x4Data[j]
        x5 = x5Data[j]
        x6 = x6Data[j]
        x7 = x7Data[j]
        x8 = x8Data[j]
        try:
            evaluatingData = eval(bestExp)
        except:
            evaluatingData = 1000000
        produced.append(evaluatingData)
    return np.square(np.subtract(produced, strengthData)).mean()

def tournament(mse):
    winners = []
    for i in range(0,len(mse)):
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

def expressionsGenerator(popul, numIterationsCrom):
    expressionsList = []
    for i in range(0, len(popul)):
        crom = popul[i]
        expr = ["e"]
        p = 0
        while not verifyEnd(expr) and p < numIterationsCrom:
            for k in range(0, len(crom)):
                j = 0
                while j < len(expr):
                    if expr[j] == "e" or expr[j] == "p" or expr[j] == "a" or expr[j] == "v":
                        break
                    j += 1

                if j == len(expr):
                    break
                else:
                     expr = updateExpression(expr, expr[j], j, k, crom)
            p += 1
        expressionsList.append(expr)
    return expressionsList

def chooseBestIndividual(popul, numIterationsCrom):
    expressionsList = expressionsGenerator(popul, numIterationsCrom)
    mse = avaliateExpressions(expressionsList)
    bestCrom = expressionsList[mse.index(min(mse))]
    return ''.join([str(elem) for elem in bestCrom])

def generateSample(bestExp):
    ### Importar dados de teste
    dataTraining = pd.read_csv("testing.csv")
    IDTest = dataTraining["ID"].tolist()
    x1Test = dataTraining["Cement"].tolist()
    x2Test = dataTraining["Blasr"].tolist()
    x3Test = dataTraining["FlyAsh"].tolist()
    x4Test = dataTraining["Water"].tolist()
    x5Test = dataTraining["Superplasticizer"].tolist()
    x6Test = dataTraining["CoarseAggregate"].tolist()
    x7Test = dataTraining["FineAggregate"].tolist()
    x8Test = dataTraining["Age"].tolist()

    csvData = []
    aux = ["ID", "strength"]
    csvData.append(aux)
    for j in range(0, len(x1Test)):
        x1 = x1Test[j]
        x2 = x2Test[j]
        x3 = x3Test[j]
        x4 = x4Test[j]
        x5 = x5Test[j]
        x6 = x6Test[j]
        x7 = x7Test[j]
        x8 = x8Test[j]
        try:
            evaluatingData = eval(bestExp)
        except:
            evaluatingData = 1000000

        aux = [IDTest[j], evaluatingData]
        csvData.append(aux)

    with open('submission.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)

    csvFile.close()

def run(numGenerations, mutationProbability, crossingProbability, numGenes, numPopulation, numIterationsCrom):
    popul = generatePopulation(numGenes, numPopulation)
    for i in range(0, numGenerations):
        expressionsList = expressionsGenerator(popul, numIterationsCrom)
        mse = avaliateExpressions(expressionsList)
        winners = tournament(mse)
        popul = crossing(popul, winners, crossingProbability)
        popul = mutation(popul, mutationProbability)

    bestExp = chooseBestIndividual(popul, numIterationsCrom)
    print(bestExp)
    print(computeErrorWithoutNormalize(bestExp))
    generateSample(bestExp)


# para executar o codigo
numIterations = 100
mutationProbability = 0.1
crossingProbability = 0.7
numGenes = 30
numPopulation = 1000
numGrammarFormation = 5
run(numIterations, mutationProbability, crossingProbability, numGenes, numPopulation, numGrammarFormation)
