### Programa
# popul = generateCromossomes(numGenes, numPopulation)
# grammarList = []
# for i in range(0, len(popul)):
#     crom = popul[i]
#     grammar = ["e"]
#
#     p = 0
#     while not verifyEnd(grammar) and p < 3:
#         for k in range(0, len(crom)):
#             j = 0
#             while j <len(grammar):
#                 if grammar[j] == "e" or grammar[j] == "o" or grammar[j] == "v":
#                     break
#                 j += 1
#
#             if j == len(grammar):
#                 break
#             else:
#                 if grammar[j] == "e":
#                     updateGrammar("e", j, k)
#                 elif grammar[j] == "o":
#                     updateGrammar("o", j, k)
#                 elif grammar[j] == "v":
#                     updateGrammar("v", j, k)
#         p +=1
#
#     grammarList.append(grammar)
#
#
# print(grammarList)
#
# mse = avaliateGrammar(grammarList)
# print(mse)
# winners = tournament(mse)
# print(winners)
#
#
# print(popul)
# popul = crossing(popul, winners)
# print(popul)
# popul = mutation(popul)
# print(popul)
