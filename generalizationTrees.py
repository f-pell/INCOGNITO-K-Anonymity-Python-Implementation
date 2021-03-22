import pandas as pd
from sharedVars import maxDatasetSize, datasetName
from graph import generateTree


data = pd.read_csv(datasetName, delimiter=';', skiprows=0, low_memory=False)
data = data.truncate(after=maxDatasetSize)

# PUT PATIENTID NODES IN ARRAY IN LEVELS
maxlength = len(str(data['PatientId'][0]))
currentlength = maxlength
patientIdGeneralizations = []
for k in range(0, maxlength):
    currentlength = currentlength - 1
    genValues = []
    for i in range(0, len(data)):
        if k == maxlength-1:
            val = str(data['PatientId'][i])
            genValues.append(val)
        else:
            val = str(data['PatientId'][i])[:-currentlength:]
            for c in range(0, currentlength):
                val = val+'*'
            genValues.append(val)

    if k != maxlength:
        uniqueVals = list(set(genValues))
        patientIdGeneralizations.append(uniqueVals)
    else:
        patientIdGeneralizations.append(genValues)

# ARRAYS CONTAIN NODES ORDERED BY LEVEL OF GENERALIZATION, FROM THE TOP TO THE BOTTOM
genderGeneralization = [['Person'],['F', 'M']]
hypertensionGeneralization = [['*'],['0', '1']]
diabetesGeneralization = [['*'],['0', '1']]
alcoholismGeneralization = [['*'],['0', '1']]
handicapGeneralization = [['*'],['0', '1', '2', '3']]
ageGeneralization = [['*'],["0-20","21-40","41-60","61-80","81-100","101-120"],["0-10","11-20","21-30","31-40","41-50","51-60","61-70","71-80","81-90","91-100","101-120"],["0-5","6-10","11-15","16-20","21-25","26-30","31-35","36-40","41-45","46-50","51-55","56-60","61-65","66-70","71-75","76-80","81-85","86-90","91-95","96-100","101-115"],["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84", "85", "86", "87", "88", "89", "90", "91", "92", "93", "94", "95", "96", "97", "98", "99", "100", "102", "115"]]
neighbourhoodGeneralization = [["Brazil"],["Vitoria","Trinidade"],['JARDIM DA PENHA','MATA DA PRAIA','PONTAL DE CAMBURI','REPÚBLICA','GOIABEIRAS','ANDORINHAS','CONQUISTA','NOVA PALESTINA','DA PENHA','TABUAZEIRO','BENTO FERREIRA','SÃO PEDRO','SANTA MARTHA','SÃO CRISTÓVÃO','MARUÍPE','GRANDE VITÓRIA','SÃO BENEDITO','ILHA DAS CAIEIRAS','SANTO ANDRÉ','SOLON BORGES','BONFIM','JARDIM CAMBURI','MARIA ORTIZ','JABOUR','ANTÔNIO HONÓRIO','RESISTÊNCIA','ILHA DE SANTA MARIA','JUCUTUQUARA','MONTE BELO','MÁRIO CYPRESTE','SANTO ANTÔNIO','BELA VISTA','PRAIA DO SUÁ','SANTA HELENA','ITARARÉ','INHANGUETÁ','UNIVERSITÁRIO','SÃO JOSÉ','REDENÇÃO','SANTA CLARA','CENTRO','PARQUE MOSCOSO','DO MOSCOSO','SANTOS DUMONT','CARATOÍRA','ARIOVALDO FAVALESSA','ILHA DO FRADE','GURIGICA','JOANA D´ARC','CONSOLAÇÃO','PRAIA DO CANTO','BOA VISTA','MORADA DE CAMBURI','SANTA LUÍZA','SANTA LÚCIA','BARRO VERMELHO','ESTRELINHA','FORTE SÃO JOÃO','FONTE GRANDE','ENSEADA DO SUÁ','SANTOS REIS','PIEDADE','JESUS DE NAZARETH','SANTA TEREZA','CRUZAMENTO','ILHA DO PRÍNCIPE','ROMÃO','COMDUSA','SANTA CECÍLIA','VILA RUBIM','DE LOURDES','DO QUADRO','DO CABRAL','HORTO','SEGURANÇA DO LAR','ILHA DO BOI','FRADINHOS','NAZARETH','AEROPORTO','ILHAS OCEÂNICAS DE TRINDADE','PARQUE INDUSTRIAL']]

print("\nGenerating generalization trees...")

print("\nGenerating gender tree...")
genderTreeLevels = len(genderGeneralization)
genderTree = generateTree(genderGeneralization, False, genderTreeLevels)
genderTree.insertEdge('Person', 'F')
genderTree.insertEdge('Person', 'M')

print("\nGenerating neighbourhood tree...")
neighbourhoodTreeLevels = len(neighbourhoodGeneralization)
neighbourhoodTree = generateTree(neighbourhoodGeneralization, False, neighbourhoodTreeLevels)
neighbourhoodTree.insertEdge('Brazil', 'Vitoria')
neighbourhoodTree.insertEdge('Brazil', 'Trinidade')
for node in neighbourhoodGeneralization[2]:
    if node != 'ILHAS OCEÂNICAS DE TRINDADE':
        neighbourhoodTree.insertEdge('Vitoria', node)
    else:
        neighbourhoodTree.insertEdge('Trinidade', node)

print("\nGenerating hypertension tree...")
hypertensionTreeLevels = len(hypertensionGeneralization)
hypertensionTree = generateTree(hypertensionGeneralization, False, hypertensionTreeLevels)
hypertensionTree.insertEdge('*', '0')
hypertensionTree.insertEdge('*', '1')

print("\nGenerating diabete tree...")
diabeteTreeLevels = len(diabetesGeneralization)
diabeteTree = generateTree(diabetesGeneralization, False, diabeteTreeLevels)
diabeteTree.insertEdge('*', '0')
diabeteTree.insertEdge('*', '1')

print("\nGenerating alcoholism tree...")
alcoholismTreeLevels = len(alcoholismGeneralization)
alcoholismTree = generateTree(alcoholismGeneralization, False, alcoholismTreeLevels)
alcoholismTree.insertEdge('*', '0')
alcoholismTree.insertEdge('*', '1')

print("\nGenerating handicap tree...")
handicapTreeLevels = len(handicapGeneralization)
handicapTree = generateTree(handicapGeneralization, False, handicapTreeLevels)
handicapTree.insertEdge('*', '0')
handicapTree.insertEdge('*', '1')
handicapTree.insertEdge('*', '2')
handicapTree.insertEdge('*', '3')

print("\nGenerating age tree...")
ageTreeLevels = len(ageGeneralization)
ageTree = generateTree(ageGeneralization, False, ageTreeLevels)
for i in range(0, len(ageGeneralization)-1):
    if i == 0:
        for node in ageGeneralization[i]:
            for nextNode in ageGeneralization[i+1]:
                    ageTree.insertEdge(node, nextNode)
    else:
       for node in ageGeneralization[i]:
            for nextNode in ageGeneralization[i+1]:
                    s1 = node.split('-')

                    s2 = nextNode.split('-')

                    s1val1 = int(s1[0])
                    s1val2 = int(s1[1])

                    if '-' in nextNode:
                        s2val1 = int(s2[0])
                        s2val2 = int(s2[1])
                    else:
                        s2val1 = int(nextNode)
                        s2val2 = int(nextNode)

                    if (s2val1 >= s1val1 and s2val1 <= s1val2) and (s2val2 >= s1val1 and s2val2 <= s1val2):
                        ageTree.insertEdge(node, nextNode)


print("\nGenerating patientIds tree...")
patientIdTreeLevels = len(patientIdGeneralizations)
patientIdTree = generateTree(patientIdGeneralizations, False, patientIdTreeLevels)
for i in range(0, len(patientIdGeneralizations)-1):
    print("#", end ="")
    if len(patientIdGeneralizations[i]) == 1:
        for node in patientIdGeneralizations[i]:
            for nextNode in patientIdGeneralizations[i+1]:
                if nextNode != node:
                    patientIdTree.insertEdge(node, nextNode)
    else:
        for node in patientIdGeneralizations[i]:
            for nextNode in patientIdGeneralizations[i+1]:
                if nextNode != node:
                    nodeSub = node[0:i+1]
                    nextSub = nextNode[0:i+1]
                    if nodeSub == nextSub:
                        patientIdTree.insertEdge(node, nextNode)


print("Done generating trees!\n")




	








