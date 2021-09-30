import copy
import math
from PIL import Image, ImageDraw
colorList = [(0,0,0),(255,0,0),(0,255,0),(0,0,255),(128,0,0),(0,128,0),(0,0,128),(255,128,0),(128,255,0),(128,0,255),(255,128,128),(255,128,255),(128,255,255),(128,255,255),(128,255,128),(128,128,255)]
def validate(rows,cols,setOPoints,point):
    xp = point[0]
    yp = point[1]
    n =(xp-1,yp)
    s= (xp+1,yp)
    e= (xp,yp+1)
    w= (xp,yp-1)
    return [x for x in [n,s,e,w] if x[0] > 0 and x[0]<=rows and x[1] > 0 and x[1] <= cols and x not in setOPoints]

def getDistance(p1,p2):
    return abs(p1[0]-p2[0])+abs(p1[1]-p2[1])

def getPair(x, cols):
    col = x % cols
    row = x // cols
    if col != 0:
        row += 1
    else:
        col = cols
    return row, col

def paint(image, x,y,color):
    print(x,y)
    for i in range(10):
        for j in range(10):
            image.putpixel((10*y+j,10*x+i),colorList[color])
    return image

def move2Point(point,pointOld,semiPaths,setOPoints,color,index1,colors):

    semiPaths[color][index1].pop(0)
    semiPaths[color][index1].insert(0, point)
    if point[0]==pointOld[0]:
        if point[1]>pointOld[1]:
            semiPaths[color][index1].append('E')
        else: semiPaths[color][index1].append('W')
    elif point[0]< pointOld[0] :
        semiPaths[color][index1].append('N')
    else:
        semiPaths[color][index1].append('S')
    if point == semiPaths[color][abs(index1-1)][0]:
        path = semiPaths[color][1]
        path.reverse()
        for step in path[:-1]:
            if step == 'N':
                semiPaths[color][0].append('S')
            elif step == 'S':
                semiPaths[color][0].append('N')
            elif step == 'E':
                semiPaths[color][0].append('W')
            else:
                semiPaths[color][0].append('E')
        semiPaths[color][1].clear()
        setOPoints.add(point)
        semiPaths[color][1].append(colors[color][0])
        semiPaths[color][0].pop(0)
        semiPaths[color][0].insert(0,colors[color][0])
    else:
        semiPaths[color][index1].pop(0)
        semiPaths[color][index1].insert(0,point)
        setOPoints.add(point)
    return semiPaths, setOPoints

def move(index1,index2,semiPaths,setOPoints,color,img,states,forced,colors):
    point = semiPaths[color][index1][0]
    point2 = semiPaths[color][index2][0]
    if point == point2:
        return semiPaths,setOPoints,False,img,states
    ok = False
    dir = validate(rows,cols,[x for x in setOPoints if x != point2],point)
    if len(dir) == 1 or (forced and len(dir)==2):
        if forced and len(dir)>1:
            states.append(move2Point(dir[1],point,copy.deepcopy(semiPaths),copy.deepcopy(setOPoints),color,index1,colors))
        ok = True
        semiPaths, setOPoints = move2Point(dir[0],point,semiPaths,setOPoints,color,index1,colors)
        #img = paint(img,fdir[0][0],fdir[0][1],color)
    return semiPaths,setOPoints,ok,img,states

def isConnected(point1, point2,rows,cols,setOPoints):
    queue = [point1]
    visitedStates = set()
    visitedStates.add(point1)
    while point1!=point2:
        if getDistance(point1,point2) == 1:
            return 2
        fdir = validate(rows,cols,setOPoints,point1)
        if len(fdir) ==0:
            queue.pop()
            if len(queue) == 0 :
                return 3
            else:
                point1 = queue[-1]
        else:
            fdir.sort(key=lambda k: getDistance(k,point2))
            visitedStates.add(fdir[0])
            queue.append((fdir[0]))
            point1 = fdir[0]
        if len(queue) == 0 :
            return 3
    return 3



g = open("output.txt", "w")
directions = {"S": (1, 0), "N": (-1, 0), "E": (0, 1), "W": (0, -1)}

f = open("level7-3.in", "r")
line = f.readline().strip()
line = line.split(" ")
tests = int(line[0])
line = line[1:]
g.write(str(tests)+" ")
for q in range(tests):
    rows = int(line[0])
    cols = int(line[1])

    im = Image.new('RGB', (rows*10+15,cols*10+15), (128, 128, 128))
    positions = int(line[2])
    colors = {}
    setOPoints = set()
    semiPaths = {}
    colorStates = {}
    line = line[3:]
    for i in range(positions):
        x = int(line[i * 2])
        color = int(line[i * 2 + 1])
        row, col = getPair(x, cols)
        setOPoints.add((row, col))
        if color not in colors.keys():
            colors[color] = [(row, col)]
            semiPaths[color] = [[(getPair(x,cols))]]
            colorStates[color] = -1
        else:
            colors[color].append((row, col))
            semiPaths[color].append([getPair(x,cols)])
    line = line[positions * 2:]
    noPaths = int(line[0])
    line = line[1:]
    for j in range(noPaths):
        color = int(line[0])
        start = int(line[1])
        length = int(line[2])
        line = line[3:]
        xstart, ystart = getPair(start, cols)
        code = 1
        setOPPoints = set()
        for k in range(length - 1):
            direction = line[k]
            xstart += directions[direction][0]
            ystart += directions[direction][1]

            if xstart <= 0 or xstart > rows or ystart <= 0 or ystart > cols or (xstart, ystart) in setOPPoints or (xstart,ystart) in setOPoints :
                code = -1
                break
            setOPPoints.add((xstart, ystart))
        if code == 1:
            direction = line[length - 1]
            xstart += directions[direction][0]
            ystart += directions[direction][1]
            if (xstart, ystart) == start or (xstart, ystart) not in colors[color]:
                code = -1
        if code == 1:
            setOPoints = setOPoints.union(setOPPoints)
            colorStates[color] = 1
        line = line[length:]
        # if q == 0:
        #     for p in setOPPoints:
        #         im =paint(im,p[0],p[1],color)

    ok = True
    # if q==0:
    #     im.show()
    states = []
    if q == 15:
        print("f")
    while ok:
        ok = False
        for color in semiPaths.keys():
            semiPaths,setOPoints,ok1,im,states = move(0,1,semiPaths,setOPoints,color,im,states,False,colors)
            semiPaths,setOPoints,ok2,im,states = move(1,0,semiPaths,setOPoints,color,im,states,False,colors)
            if ok1 or ok2:
                ok = True
        if not ok:
            for color in semiPaths.keys():
                semiPaths,setOPoints,ok1,im,states = move(0,1,semiPaths,setOPoints,color,im,states,True,colors)
                # semiPaths,setOPoints,ok2,im,states = move(1,0,semiPaths,setOPoints,color,im,states,True,colors)
                if ok1 :#:or ok2:
                    ok = True
                    break
        if not ok:
            isComplete = True
            for color in range(1,len(colors)+1):
                isComplete = isComplete and semiPaths[color][0][0] == semiPaths[color][1][0]
            if not ok and not isComplete :
                ok = True
                semiPaths,setOPoints = states.pop()
    index= 0
    for color in semiPaths.keys():
        if len(semiPaths[color][0])>1:
            index += 1
        if len(semiPaths[color][1])>1:
            index += 1
    g.write(str(index)+ " ")
    for color in semiPaths.keys():
        if len(semiPaths[color][0])>1:
            g.write(str(color)+ " "+ str((colors[color][0][0]-1)*cols +colors[color][0][1] ) +" "+ str(len(semiPaths[color][0][1:]))+" ")
            for pp in semiPaths[color][0][1:]:
                g.write(str(pp) + " ")
        if len(semiPaths[color][1])>1:
            g.write(str(color)+ " "+ str((colors[color][1][0]-1)*cols +colors[color][1][1]) +" "+ str(len(semiPaths[color][1][1:]))+" ")
            for pp in semiPaths[color][1][1:]:
                g.write(str(pp) + " ")


# #im.show()
#     x = list(colorStates.keys())
#     x.sort()
#     for xx in x:
#         g.write(str(colorStates[xx])+ " ")
#         print(str(colorStates[xx])+ " ", sep="")