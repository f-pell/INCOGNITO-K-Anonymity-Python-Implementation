from generalizationTrees import patientIdTree, genderTree, neighbourhoodTree, hypertensionTree, diabeteTree, alcoholismTree, handicapTree, ageTree
from graph import generateGraph
from sharedVars import kValue
import itertools

# RETURN COUNT * GROUP BY XXX SO K ANONYMITY COUNT DATA
def getFrequencySet(anonymizedData, columns):
    datacolumns = ['AppointmentId']
    for i in columns:
        datacolumns.append(i)
    kvalue = anonymizedData[datacolumns].groupby(columns).agg(['count'])
    return kvalue

# CHECKS IF DATA IS K-ANONYMOUS
def isKAnonymized(kvalue, data):
    isAnonymized = True

    for i in range(0, len(data)):
        if data.iloc[i, 0] < int(kvalue):
            isAnonymized = False
    return isAnonymized

# ANONYMIZES DATA COMBINATIONS
def anonymizeCombination(dataToAnonymize, key, reachLevel):

    for curLevel in range(0, reachLevel):
        if key == 'PatientId':
            if curLevel < patientIdTree.returnMaxTreeHeight()-1: # We check if we have reached the root node
                for index, row in dataToAnonymize.iterrows():
                    node = row[key]
                    #if patientIdTree.isNodeRoot(node) == False:
                    edgesList = patientIdTree.getNodeEdges(node)
                    dataToAnonymize.loc[dataToAnonymize.PatientId==node, 'PatientId'] = edgesList[0].c1Value
                    #else:
                       # return dataToAnonymize, False
            else:
                return dataToAnonymize, False

        if key == 'Neighbourhood':
            if curLevel < neighbourhoodTree.returnMaxTreeHeight()-1:
                for index, row in dataToAnonymize.iterrows():
                    node = row[key]
                    #if neighbourhoodTree.isNodeRoot(node) == False:
                    edgesList = neighbourhoodTree.getNodeEdges(node)
                    dataToAnonymize.loc[dataToAnonymize.Neighbourhood==node, 'Neighbourhood'] = edgesList[0].c1Value
                    #else:
                     #   return dataToAnonymize, False
            else:
                return dataToAnonymize, False

        if key == 'Diabetes':
            if curLevel < diabeteTree.returnMaxTreeHeight()-1:
                for index, row in dataToAnonymize.iterrows():
                    node = row[key]
                    #if diabeteTree.isNodeRoot(node) == False:
                    edgesList = diabeteTree.getNodeEdges(node)
                    dataToAnonymize.loc[dataToAnonymize.Diabetes==node, 'Diabetes'] = edgesList[0].c1Value
                    #else:
                      #  return dataToAnonymize, False
            else:
                return dataToAnonymize, False


        if key == 'Alcoholism':
            if curLevel < alcoholismTree.returnMaxTreeHeight()-1:
                for index, row in dataToAnonymize.iterrows():
                    node = row[key]
                    #if alcoholismTree.isNodeRoot(node) == False:
                    edgesList = alcoholismTree.getNodeEdges(node)
                    dataToAnonymize.loc[dataToAnonymize.Alcoholism==node, 'Alcoholism'] = edgesList[0].c1Value
                    #else:
                     #   return dataToAnonymize, False
            else:
                return dataToAnonymize, False


        if key == 'Hypertension':
            if curLevel < hypertensionTree.returnMaxTreeHeight()-1:
                for index, row in dataToAnonymize.iterrows():
                    node = row[key]
                    #if hypertensionTree.isNodeRoot(node) == False:
                    edgesList = hypertensionTree.getNodeEdges(node)
                    dataToAnonymize.loc[dataToAnonymize.Hypertension==node, 'Hypertension'] = edgesList[0].c1Value
                    #else:
                     #   return dataToAnonymize, False
            else:
                return dataToAnonymize, False


        if key == 'Handicap':
            if curLevel < handicapTree.returnMaxTreeHeight()-1:
                for index, row in dataToAnonymize.iterrows():
                    node = row[key]
                    #if handicapTree.isNodeRoot(node) == False:
                    edgesList = handicapTree.getNodeEdges(node)
                    dataToAnonymize.loc[dataToAnonymize.Handicap==node, 'Handicap'] = edgesList[0].c1Value
                    #else:
                    #    return dataToAnonymize, False
            else:
                return dataToAnonymize, False


        if key == 'Age':
            if curLevel < ageTree.returnMaxTreeHeight()-1:
                for index, row in dataToAnonymize.iterrows():
                    node = row[key]
                    #if ageTree.isNodeRoot(node) == False:
                    edgesList = ageTree.getNodeEdges(node)
                    dataToAnonymize.loc[dataToAnonymize.Age==node, 'Age'] = edgesList[0].c1Value
                    #else:
                     #   return dataToAnonymize, False
            else:
                return dataToAnonymize, False


        if key == 'Gender':
            if curLevel < genderTree.returnMaxTreeHeight()-1:
                for index, row in dataToAnonymize.iterrows():
                    node = row[key]
                    #if genderTree.isNodeRoot(node) == False:
                    edgesList = genderTree.getNodeEdges(node)
                    dataToAnonymize.loc[dataToAnonymize.Gender==node, 'Gender'] = edgesList[0].c1Value
                    #else:
                    #    return dataToAnonymize, False
            else:
                return dataToAnonymize, False

    return dataToAnonymize, True

# RUNS ANONYMIZATION FOR EACH QI IN THE COMBINATION
def generalizeData(node, data):
    keys = []
    levels = []
    for y in node:
        val = y.split('-')
        key = val[0]
        level = int(val[1])

        if key == 'p':
            key = 'PatientId'
        if key == 'g':
            key = 'Gender'
        if key == 'age':
            key = 'Age'
        if key == 'n':
            key = 'Neighbourhood'
        if key == 'h':
            key = 'Hypertension'
        if key == 'd':
            key = 'Diabetes'
        if key == 'a':
            key = 'Alcoholism'
        if key == 'hc':
            key = 'Handicap'
        
        keys.append(key)
        levels.append(level)
        if level != 0:
            data, done = anonymizeCombination(data, key, level)

    return data, keys, levels # levels is used only for printing purposes


# GENERATES A GRAPH FROM A COMBINATION
def graphFromCombinations(combinations):
    resultingCombinations = []
    for comb in combinations:
        maxSumm = 0
        for v in comb:
            summ = 0
            for k in v:
                val = k.split('-')
                summ = summ+int(val[1])
            if summ > maxSumm:
                maxSumm = summ

        igraph = generateGraph([comb], False)
        resultingCombinations.append(igraph)
    return resultingCombinations

# A PRIORI PRUNING
def performAPrioriPruning(remainingNodes, newTuples):
    print(" Remaining nodes "+str(remainingNodes))
    print(" Generated tuples "+str(newTuples))
    indexesToRemove = []

    for i in range(0, len(newTuples)):
        for comb in itertools.combinations(newTuples[i], len(newTuples[i])-1):
            toCheck = list(comb)
            print("Tup comb "+str(toCheck))
            if toCheck not in remainingNodes:
                indexesToRemove.append(i)

        print("\n")

    indexesToRemove = list(set(indexesToRemove))
    for index in sorted(indexesToRemove, reverse=True):
            newTuples.pop(index)
    print(" Pruned tuples "+str(newTuples))

    return newTuples


# DISCARDS NODES THAT ARE NOT K-ANONYMOUS AND RETURNS THE K-ANONYMOUS NODES
def discardNonKLevels(combs, k, editedData, i):

    finalList = []
    counter = 0
    for graph in combs:
        nodesSortedPerHeight = []

        print("\n#####################")
        print(" Analyzing new graph")
        print(" "+str(counter)+" of "+str(len(combs)))
        print("#####################\n")

        counter = counter + 1

        for i in graph.graphDict:
            nodesSortedPerHeight.append(i)

        def getHeight(node):
            return graph.getNodeHeight(node)

        indexesToRemove = []

        nodesSortedPerHeight.sort(key=getHeight)
        nodesSortedPerHeight.reverse()
        heights = []

        for n in nodesSortedPerHeight:
            heights.append(getHeight(n))

        for i in range(0, len(nodesSortedPerHeight)):


            if nodesSortedPerHeight[i].wasVisited == False:

                copyOfData = editedData.copy()
                
                keys = []
                levels = []

                copyOfData, keys, levels = generalizeData(nodesSortedPerHeight[i].returnValue(), copyOfData)

                kAnVal = getFrequencySet(copyOfData, keys)
                if isKAnonymized(kValue, kAnVal) == False:
                    
                    print(str(keys)+" level(s) "+str(levels)+" not anonymous, discarding...")
                    indexesToRemove.append(i)
                else:
                    print(str(keys)+" level "+str(levels)+" is anonymous")
                    nodesSortedPerHeight[i].wasVisited == True

                    #print("node "+str(nodesSortedPerHeight[i].returnValue())+" height "+str(heights[i])+" max h "+str(len(nodesSortedPerHeight)-1))

                    if heights.count(heights[i]) == 1 and heights[i] == len(nodesSortedPerHeight)-1:
                        for n1 in nodesSortedPerHeight:
                            n1.wasVisited = True
                            # mark all generalizations of root
                            #print("set as root")
                    else:
                        generalizations = graph.getNodeGeneralizations(nodesSortedPerHeight[i])
                        for n1 in generalizations:
                            for n2 in nodesSortedPerHeight:
                                if n1 == n2.returnValue():
                                    n2.wasVisited = True
                                    #print("set as generalization")
                                    # mark all generalizations of a node
                    

        for index in sorted(indexesToRemove, reverse=True):
            nodesSortedPerHeight.pop(index)

        vals = []
        for x in nodesSortedPerHeight:
            vals.append(x.returnValue())

        finalList.append(vals)

        print("#####################\n")

    combs = finalList

    return combs
    










