from enum import Enum

f = open("input.txt", "r")
line = f.readline()
lines = line.split(" ")
l = int(lines[0])
suma = 0
j = 1
coord = (0, 0)
minX = 0
minY = 0
maxX = 0
maxY = 0
dir = [[(0, -1), (-1, 0), (0, 1)],
       [(-1, 0), (0, 1), (1, 0)],
       [(0, 1), (1, 0), (0, -1)],
       [(1, 0), (0, -1), (-1, 0)]
       ]
dic = {}
dic2 = {}
dic3 = {}


class Orientation(Enum):
    LEFT = 0
    FORWARD = 1
    RIGHT = 2
    BACKWARD = 3


def turn(orientation, dir):
    if dir == 'L':
        if orientation == Orientation.LEFT:
            return Orientation.BACKWARD
        elif orientation == Orientation.RIGHT:
            return Orientation.FORWARD
        elif orientation == Orientation.BACKWARD:
            return Orientation.RIGHT
        return Orientation.LEFT
    elif dir == 'R':
        if orientation == Orientation.LEFT:
            return Orientation.FORWARD
        elif orientation == Orientation.RIGHT:
            return Orientation.BACKWARD
        elif orientation == Orientation.BACKWARD:
            return Orientation.LEFT
        return Orientation.RIGHT
    return orientation


# dic[0] = [0]
isFirst = True
o = Orientation.FORWARD
temp = []

for i in range(l):

    s = lines[j]
    x = int(lines[j + 1])

    for k in range(x):
        for index in range(len(s)):
            ch = s[index]
            prevO = o
            o = turn(o, ch)
            if coord[1] not in dic.keys():
                dic[coord[1]] = []
            if coord[1] not in dic2.keys():
                dic2[coord[1]] = []
            if coord[0] not in dic3.keys():
                dic3[coord[0]] = []
            if ch == 'F':
                if coord[0] not in dic2[coord[1]]:
                    dic2[coord[1]].append(coord[0])
                if coord[1] not in dic3[coord[0]]:
                    dic3[coord[0]].append(coord[1])
                fx = dir[o.value][1][0]
                fy = dir[o.value][1][1]
                coord = (coord[0] + fx, coord[1] + fy)
                if maxY < coord[1]:
                    maxY = coord[1]
                if maxX < coord[0]:
                    maxX = coord[0]
                if minY > coord[1]:
                    minY = coord[1]
                if minX > coord[0]:
                    minX = coord[0]
            elif coord[0] not in dic[coord[1]]:
                t = k == x-1 and index == len(s)-1 and i == l-1
                if (not t):
                    dic[coord[1]].append(coord[0])


    j += 2
    suma += s.count('F') * x

xs = 1 if abs(minX) + maxX == 0 else abs(minX) + maxX
ys = 1 if abs(minY) + maxY == 0 else abs(minY) + maxY
aria = 0
prev = []
if len(dic[0])%2!=0:
    dic[0].append(0)
if len(dic2[0])%2!=0:
    dic2[0].append(0)
computedHoles = []
totalHoles= 0
for i in range(maxY, minY, -1):
    v = dic[i]
    newL = [x for x in v if x not in prev]
    newL.extend(x for x in prev if x not in v)
    newL.sort()
    if len(newL) == 0:
        continue
    prev = newL
    prevCoord = newL[0]
    for e in range(len(newL)//2):
        q = newL[2*e]
        qq = newL[2*e+1]
        aria += abs(qq-q)
    print (aria,newL)

pocketAria = xs*ys - aria
nonPokets = []
for i in range(maxX, minX-1,-1):
    v = dic3[i]
    v.sort()
    minp = v[0]
    maxp = v[-1]
    for k in range (minY,minp):
        vv = dic2[k]
        vv.sort()
        minpv = vv[0]
        maxpv = vv[-1]
        tt = minpv < i and maxpv > i
        if not tt:
            pocketAria -= 1
    for k in range (maxp+1,maxY+1):
        vv = dic2[k]
        vv.sort()
        minpv = vv[0]
        maxpv = vv[-1]
        tt = minpv < i and maxpv > i
        if not tt:
            pocketAria -= 1

print(suma, xs * ys, aria, pocketAria)
