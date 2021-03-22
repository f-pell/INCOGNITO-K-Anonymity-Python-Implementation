import pandas as pd
import itertools
from utilities import getFrequencySet, isKAnonymized, anonymizeCombination, generalizeData, graphFromCombinations, discardNonKLevels
from sharedVars import kValue, maxDatasetSize, datasetName, outputName, quasiIdentifiers, combs0
from graph import generateGraph
import time

# READ CSV DATA
csvData = pd.read_csv(datasetName, delimiter=';', skiprows=0, low_memory=False)
csvData = csvData.truncate(after=maxDatasetSize)

# DATA TO ANONYMIZE
editedData = csvData.copy()

resultingCombinations = graphFromCombinations(combs0)

finalGraph = []
start = time.time()

for i in range(0, len(quasiIdentifiers)):

    resultingCombinations = discardNonKLevels(resultingCombinations, kValue, editedData, i)

    if i != len(quasiIdentifiers)-1:

        if type(resultingCombinations[0]) == list:
            resultingCombinations = [j for s in resultingCombinations for j in s]
            resultingCombinations = [j for s in resultingCombinations for j in s]
            resultingCombinations = list(set(resultingCombinations))

        l = []
        for comb in  itertools.combinations(resultingCombinations, i+2):
            l.append(list(comb))
        resultingCombinations = l

        # REMOVE key DUPLICATES

        indexesToRemove = []
        for c in range(0, len(resultingCombinations)):
            checkingDuplicatesArr = []
            
            for x in resultingCombinations[c]:
                val = x.split('-')
                key = val[0]
                checkingDuplicatesArr.append(key)

            if len(set(checkingDuplicatesArr)) != len(checkingDuplicatesArr):
                indexesToRemove.append(c)

            resultingCombinations[c] = sorted(resultingCombinations[c])

        for index in sorted(indexesToRemove, reverse=True):
                #print("removing duplicates"+str(index))
                resultingCombinations.pop(index)

        resultingCombinations = sorted(resultingCombinations)

        # REMOVE node DUPLICATES

        nodesToRemove = []
        for n in range(0, len(resultingCombinations)):
            node = resultingCombinations[n]
            for m in range(0, len(resultingCombinations)):
                node2 = resultingCombinations[m]
                if node == node2 and m != n:
                    #print(str(node)+" = "+str(m))
                    nodesToRemove.append(n)

        for index in sorted(nodesToRemove, reverse=True):
                resultingCombinations.pop(index)          
    else:
        resultingCombinations = [j for s in resultingCombinations for j in s]

    # ORGANIZE NODES
    graphs = []
    for c in resultingCombinations:
        values = []
        keys = []
        for x in c:
            val = x.split('-')
            keys.append(val[0])

        skip = False
        for t in graphs:
            for y in t:
                test_keys = []
                for x in range(0, len(t)):
                    for m in t[x]:
                        val = m.split('-')
                        test_keys.append(val[0])
                    break
                if test_keys == keys:
                    skip = True
                break
            if skip == True:
                break

        if skip == False:
            for p in resultingCombinations:
                sub_keys = []
                for x in p:
                    val = x.split('-')
                    sub_keys.append(val[0])
                if sub_keys == keys:
                    values.append(p)
            graphs.append(values)
            
    # BUILD NEXT GRAPHS MADE OF i COMBINATIONS WITH THEIR EDGES
    resultingCombinations = graphFromCombinations(graphs)

    elapsed = (time.time() - start)
    print("Iteration done in... "+str(time.strftime("%H:%M:%S", time.gmtime(elapsed))))

    finalGraph = resultingCombinations



elapsed = (time.time() - start)
print("INCOGNITO Done in... "+str(time.strftime("%H:%M:%S", time.gmtime(elapsed))))



print("Final graph "+str(finalGraph))
for graph in finalGraph:
    graph.printGraph()


print("Testing bottom node k-anonymity...")
graph = finalGraph[0]
nodeToTest = ""
maxH = 0
graphHeight = graph.getGraphHeight()
print("Graph height "+str(graphHeight))
for node in graph.graphDict:
    nodeH = graph.getNodeHeight(node)
    found = False
    if nodeH == graphHeight-1:
        nodeToTest = node.returnValue()
        found = True
    print("Node "+str(node.returnValue())+" height is... "+str(nodeH))
    if found == True:
       break
    
keys = []
levels = []
editedData, keys, levels = generalizeData(nodeToTest, editedData)

gkav = getFrequencySet(editedData, keys)
print(gkav)
if isKAnonymized(kValue, gkav) == True:
    print(str(keys)+" level "+str(levels)+" is anonymous")
    print("INCOGNITO succeded!")
    print("result anonymized with node "+str(nodeToTest)+" was saved as "+outputName)
    editedData.to_csv(outputName, sep=';')
else:
    print("Error")




	








