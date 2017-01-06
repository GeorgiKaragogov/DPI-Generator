import math
import string
import random
from Tkinter import Tk
from tkFileDialog import askopenfilename

Tk().withdraw()

def ReadFile(Directory):
    file = open(Directory,'r')
    lines = file.read().split('\n')

    mainArray = []
    j = 0
    for line in lines:
        mainArray.append([])
        elements = line.split(' ')
        for el in elements:
            mainArray[j].append(el)
        j = j + 1

    return mainArray

def DirectionAngle(Xi,Yi,Xj,Yj):
    dY = Yj - Yi
    dX = Xj - Xi

    ro = 200 / (math.pi)
    alfat = math.atan(abs(dY/dX))*ro
    sdY = Sign(dY)
    sdX = Sign(dX)
    alfa = 0
    if (dY == 0 and dX == 0):
        print("Error - Points with equal coordinates")
    elif(dY == 0 and dX != 0):
        if (dX > 0):
            alfa = 0
        else:
            alfa = 200
    elif(dY != 0 and dX ==0):
        if (dY > 0):
            alfa = 100
        else:
            alfa = 300
    elif(dY != 0 and dX !=0):
        if (sdY > 0 and sdX > 0):
            alfa = alfat
        elif(sdY > 0 and sdX < 0):
            alfa = 200 - alfat
        elif(sdY < 0 and sdX < 0):
            alfa = 200 + alfat
        elif(sdY < 0 and sdX > 0):
            alfa = 400 - alfat

    return alfa

def findRow(index,pointsArray):
    foundRow = []
    for i in range(0,len(pointsArray),1):
        if (index == pointsArray[i][0]):
            foundRow.append(pointsArray[i])
            return foundRow

def GenMeas(configuration, pointsArray, instrumentHeight, signalHeight):
    ro = 200 / (math.pi)
    genDirAngles = []
    genDirections = []
    genDistances = []
    genZenitAngles = []

    stX = foundRow = findRow(configuration[0],pointsArray)[0][1]
    stY = foundRow = findRow(configuration[0],pointsArray)[0][2]
    stZ = foundRow = findRow(configuration[0],pointsArray)[0][3]
    instrumentHeight = instrumentHeight + random.randint(-99,99)*0.001
    for i in range(1,len(configuration),1):

        mX = findRow(configuration[i],pointsArray)[0][1]
        mY = findRow(configuration[i],pointsArray)[0][2]
        mZ = findRow(configuration[i], pointsArray)[0][3]
        alfa = DirectionAngle(stX,stY,mX,mY)
        genDirAngles.append(alfa)

        distance = math.sqrt(math.pow((mX - stX),2) + math.pow(mY - stY,2))

        dH = mZ - stZ
        cotgZ = (dH + signalHeight - instrumentHeight)/distance
        tgZ = 1/cotgZ
        Z = math.atan(tgZ)*ro
        if (Z < 0):
            Z = Z + 200

        slopeDistance = distance/math.sin(Z/ro)
        genZenitAngles.append(Z)
        genDistances.append(slopeDistance)


    for i in range(0,len(genDirAngles),1):
        direction = genDirAngles[i] - genDirAngles[0]
        if (direction < 0):
            direction = direction + 400
        genDirections.append(direction)
    return genDirections,genZenitAngles,genDistances,instrumentHeight

def StationString(configuration, pointsArray, instrumentHeight, signalHeight):
    directions, zenitAngles, distances, instrumentHeight = GenMeas(configuration, pointsArray, instrumentHeight, signalHeight)

    firstRow = '{:<6} {:04.3f}'.format(configuration[0],instrumentHeight)
    allRows = []
    allRows.append(firstRow)
    for i in range(0,len(directions),1):
        direction = directions[i]
        zenitAngle = zenitAngles[i]
        distance = distances[i]


        if (direction >= 200):
            direction2 = direction - 200
        else:
            direction2 = direction + 200

        direction2 = direction2 + random.randint(-3,3)*0.001

        zenitAngle2 = 400-zenitAngle + random.randint(-4,4)*0.001
        distance2 = distance + random.randint(-9,9)*0.001


        if (i == len(directions) - 1):
            middleRow = '{:<6} {:.3f} {:.4f} {:.4f} {:.3f}'.format(configuration[i + 1], signalHeight,direction, zenitAngle, distance)
            middleRow2 ='{:<6} {:.3f} {:.4f} {:.4f} {:.3f}*'.format(configuration[i + 1], signalHeight,direction2, zenitAngle2, distance2)
        else:
            middleRow = '{:<6} {:.3f} {:.4f} {:.4f} {:.3f}'.format(configuration[i+1],signalHeight,direction,zenitAngle,distance)
            middleRow2 = '{:<6} {:.3f} {:.4f} {:.4f} {:.3f}'.format(configuration[i + 1], signalHeight, direction2,zenitAngle2, distance2)

        if (int(configuration[i + 1]) < 10000):
            allRows.append(middleRow)
        else:
            allRows.append(middleRow)
            allRows.append(middleRow2)

    return allRows

def KorString(pointsArray):

    korFile = []
    for i in range(0,len(pointsArray),1):
        if (int(pointsArray[i][0]) < 110000 and int(pointsArray[i][0]) > 100000):
            korRow = '{} 4 {:.3f} {:.3f} 5 {:.3f} 0.0 0.0 0.0 0.0\n'.format(pointsArray[i][0],pointsArray[i][1],pointsArray[i][2],pointsArray[i][3])
            korFile.append(korRow)
    return korFile

def Sign(number):
    try:return number/abs(number)
    except ZeroDivisionError:return 0


fileDirectory = askopenfilename()
mainArray = ReadFile(fileDirectory)
mainFile = open(fileDirectory,'r')
mainFileName = string.replace(mainFile.name,'.txt','')

instrumentHeigth = float(mainArray[0][2])
signalHeigth = float(mainArray[0][3])

ro = 200/(math.pi)

amountPoints = int(mainArray[0][0])
amountStations = int(mainArray[0][1])

points = []

for i in range(0,amountPoints,1):
    points.append([mainArray[i + 1][0],float(mainArray[i + 1][1]),float(mainArray[i + 1][2]),float(mainArray[i + 1][3])])

configuration = []

for i in range(0,amountStations,1):
    locConf = []
    for j in range(0,len(mainArray[i+1+amountPoints]),1):
        locConf.append(mainArray[i+1+amountPoints][j])
    configuration.append(locConf)
    del locConf

dpi_file = open(mainFileName + ".dpi","w")
dpi_file.write("%s\n" % "")
dpi_file.write("%s\n" % "")
dpi_file.write("%s\n" % "")
localConfiguration = []
for i in range(0,amountStations,1):
    localConfiguration = configuration[i]
    currentStation = StationString(localConfiguration,points,instrumentHeigth,signalHeigth)
    for j in range(0,len(currentStation),1):
        dpi_file.write("%s\n" % currentStation[j])
dpi_file.close()

kor_file = open(mainFileName + ".kor", "w")
kor_file.write("%s\n" % "")
kor_file.write("%s\n" % "")
kor_file.write("%s\n" % "")

korData = KorString(points)
for i in range(0,len(korData),1):
    kor_file.write("%s" % korData[i])
kor_file.close()

