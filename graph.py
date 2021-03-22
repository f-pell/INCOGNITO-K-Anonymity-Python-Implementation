import pandas as pd
import itertools

class Node(object):
    def __init__(self, value, isRoot):
            self.value = value
            self.isRoot = isRoot
            self.wasVisited = False
            
    # RETURNS THE NAME OF THE NODE i.e. PatientID -> 5523343
    def returnValue(self):
            return self.value

class Edge(object):
    def __init__(self, c1Value, c2Value):
            self.c1Value = c1Value
            self.c2Value = c2Value

class GraphOrTree(object):

    # CONTAINS A DICT WITH ALL THE NODES AND THEIR EDGES
    # HAS A TOTAL HEIGHT ONLY WHEN USED AS A TREE
    def __init__(self, totalTreeHeight):
            self.graphDict = {}
            self.totalHeight = totalTreeHeight


    def returnMaxTreeHeight(self):
        return self.totalHeight

    # CHECK IF THE NODE IS A ROOT IN A TREE ENVIRONMENT
    def isNodeRoot(self, node):
        for i in self.graphDict:
                if str(i.returnValue()) == str(node):
                    return i.isRoot

    # INSERTS AN EDGE
    def insertEdge(self, c1Value, c2Value):

            c1Available = False
            c2Available = False

            edgesc1 = []
            edgesc2 = []
            
            for i in self.graphDict:
                    if i.returnValue() == c1Value:
                            #print("C1 Node available")
                            c1Available = True
                            edgesc1 = self.graphDict[i]

            for i in self.graphDict:
                    if i.returnValue() == c2Value:
                            #print("C2 Node available")
                            c2Available = True
                            edgesc2 = self.graphDict[i]

            if c1Available and c2Available:
                edgesc1.append(Edge(c1Value, c2Value))
                edgesc2.append(Edge(c1Value, c2Value))
            
    # ADDS A NODE IN A TREE ENVIRONMENT
    def insertTreeNode(self, value, isRoot, duplicateCheck):
            if duplicateCheck == True:
                alreadyPresent = False
                for i in self.graphDict:
                        if i.returnValue() == value:
                                alreadyPresent = True
                                print("Value already added")
                                break
                if alreadyPresent == False:
                        self.graphDict[Node(value, isRoot)] = []
            else:
                self.graphDict[Node(value, isRoot)] = []

    # RETURNS A NODE HEIGHT
    def searchRecursiveHeight(self, node, summ, height):
        for x in self.graphDict:
                if x.returnValue() == node:
                    totalEdges = []
                    edgesList = self.getNodeEdges(x.returnValue())
                    for i in edgesList:
                        if i.c1Value not in totalEdges and i.c1Value != x.returnValue():
                            totalEdges.append(i.c1Value)
                        if i.c2Value not in totalEdges and i.c2Value != x.returnValue():
                            totalEdges.append(i.c2Value)

                    totalEdges.sort()

                    if len(totalEdges) > 0:
                        
                        foundNode = False
                        finalNextSumm = 0
                        nextNode = ""
                        for node in totalEdges:
                            nextSumm = 0
                            for vals in node:
                                val = vals.split('-')
                                nextSumm = nextSumm+int(val[1])
                            if nextSumm > summ:
                                foundNode = True
                                nextNode = node
                                finalNextSumm = nextSumm
                            if foundNode == True:
                                break
                        if foundNode == True:
                            height = height + 1
                            if nextSumm != summ:
                                height = self.searchRecursiveHeight(nextNode, nextSumm, height)        

                    return height

    # RETURNS TOTAL GRAPH HEIGHT
    def getGraphHeight(self):
        minSumm = 999
        selectedNode = Node(0, False)

        if len(self.graphDict) == 0:
                print("No nodes!")
                return 0

        if len(self.graphDict) == 1:
            print("Just one node!")
            return 1

        for node in self.graphDict:
            summ = 0
            for vals in node.returnValue():
                val = vals.split('-')
                summ = summ+int(val[1])
            if summ < minSumm:
                minSumm = summ
                selectedNode = node
        height = 0

        height = self.searchRecursiveHeight(selectedNode.returnValue(), minSumm, height)
        return (height+1)


    # RETURNS NODE HEIGHT
    def getNodeHeight(self, node):

        summ = 0
        for vals in node.returnValue():
            val = vals.split('-')
            summ = summ+int(val[1])
        height = 0
        height = self.searchRecursiveHeight(node.returnValue(), summ, height)

        return height

    # PERFORMS A RECURSIVE SEARCH ON A NODE IN ORDER TO GET ALL ITS GENERALIZATIONS
    def searchRecursiveGeneralizations(self, node, summ, generalizations):

        for x in self.graphDict:
                if x.returnValue() == node:
                    totalEdges = []
                    edgesList = self.getNodeEdges(x.returnValue())
                    for i in edgesList:
                        if i.c1Value not in totalEdges and i.c1Value != x.returnValue():
                            totalEdges.append(i.c1Value)
                        if i.c2Value not in totalEdges and i.c2Value != x.returnValue():
                            totalEdges.append(i.c2Value)

                    totalEdges.sort()

                    if len(totalEdges) > 0:
                        
                        nextNodes = []
                        maxSumm = -99

                        for node in totalEdges:
                            nextSumm = 0
                            for vals in node:
                                val = vals.split('-')
                                nextSumm = nextSumm+int(val[1])
                            if nextSumm > summ:
                                nextNodes.append(node)
                                if nextSumm > maxSumm:
                                    maxSumm = nextSumm

                        if maxSumm == -99:
                            return generalizations
                        elif maxSumm != summ:
                            summ = maxSumm
                            for node in nextNodes:
                                generalizations.append(node)
                                generalizations = self.searchRecursiveGeneralizations(node, summ, generalizations)  
                        

    # RETURNS ALL THE GENERALIZATIONS OF A NODE
    def getNodeGeneralizations(self, node):
        generalizations = []
        initialSumm = 0
        for vals in node.returnValue():
            val = vals.split('-')
            initialSumm = initialSumm+int(val[1])
        generalizations = self.searchRecursiveGeneralizations(node.returnValue(), initialSumm, generalizations)
        generalizations.sort()
        generalizations = list(generalizations for generalizations,_ in itertools.groupby(generalizations))
        return generalizations

    # RETURNS NODE EDGES IN A GRAPH ENVIRONMENT
    def getNodeEdges(self, node):
            for i in self.graphDict:
                if str(i.returnValue()) == str(node):
                    return self.graphDict[i]

    # INSERTS A NODE IN A GRAPH ENVIRONMENT
    def insertGraphNode(self, value):
            self.graphDict[Node(value, False)] = []


    def printEdge(self, edge):
            print("------")
            if len(edge) > 0:
                for i in edge:
                        print("Edge Nodes: ["+str(i.c1Value)+", "+str(i.c2Value)+"]")
            else:
                print("None")
            print("------")

    def printGraph(self):
            for i in self.graphDict:
                    print("Node: "+str(i.returnValue())+ " isRoot "+str(i.isRoot))
                    self.printEdge(self.graphDict[i])


    # RETURNS THE SUMM OF ALL NODE GENERALIZATIONS
    def getNodeSumm(self, node):
        summ = 0
        for vals in node.returnValue():
            val = vals.split('-')
            summ = summ+int(val[1])
        return summ

def generateTree(nodesList, duplicateCheck, totalHeight):
    result = GraphOrTree(totalHeight)
    levels = len(nodesList)
    print("Levels "+str(levels))
    for i in range(0, levels):
        print("#", end ="")
        if(len(nodesList[i]) == 1):
            for node in nodesList[i]:
                result.insertTreeNode(node, True, duplicateCheck)
        else:
            for node in nodesList[i]:
                result.insertTreeNode(node, False, duplicateCheck)

    return result

# CHECKS THE DIFFERENCE BETWEEN TWO CONNECTED NODES
def nodesDifferenceCheck(n1, n2):

    n1a = []
    n2a = []
    for vals in n1.returnValue():
        val = vals.split('-')            
        n1a.append(int(val[1]))
    for vals in n2.returnValue():
        val = vals.split('-')            
        n2a.append(int(val[1]))

    for i in range(0, len(n1a)):
        if n2a[i]-n1a[i] < 0:
            return False
    return True

def generateGraph(nodesList, duplicateCheck):
    result = GraphOrTree(0)
    
    for node in nodesList:
        for nodeValue in node:
            result.insertGraphNode(nodeValue)


    addedEdges = []
    for i in result.graphDict:
        for j in result.graphDict:
            skip = False

            for c in addedEdges:
                if (c[0] == i.returnValue() and c[1] == j.returnValue()) or (c[1] == i.returnValue() and c[0] == j.returnValue()):
                    skip = True

            if skip == False:
                if i != j:
                    hi = result.getNodeSumm(i)
                    hj = result.getNodeSumm(j)
                    if abs(hi-hj) == 1:
                        if nodesDifferenceCheck(i, j) == True:
                            result.insertEdge(i.returnValue(), j.returnValue())
                            couple = []
                            couple.append(i.returnValue())
                            couple.append(j.returnValue())
                            addedEdges.append(couple)

    print("Generating graph with height "+str(result.getGraphHeight()))

    return result

	








