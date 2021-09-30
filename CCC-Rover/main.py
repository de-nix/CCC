import math
import requests

def computeCoords(whB, prevSteer, distance,steeringAngle):
    if steeringAngle == 0 :
        x = 0
        y = distance
        newD= 0
    else:
        radius = whB/ math.sin(math.radians(abs(steeringAngle)))
        circleP = 2*math.pi*radius
        sign = 1 if distance>0 else -1
        while abs(distance) > circleP:
            distance -= circleP*sign
        formedAngle = distance/radius if distance>0 else (2*math.pi - abs(distance)/radius)
        x = radius - math.cos(formedAngle) * radius if steeringAngle>0 else math.cos(formedAngle) * radius -radius
        y = math.sin(formedAngle)*radius
        formedAngle = math.degrees(formedAngle) if steeringAngle>0 else 360 - math.degrees(formedAngle)
        newD = formedAngle
    xx = math.cos(math.radians(abs(prevSteer)))*x + math.sin(math.radians(abs(prevSteer)))*y
    yy = -math.sin(math.radians(abs(prevSteer)))*x +math.cos(math.radians(abs(prevSteer)))*y
    return xx,yy,newD

def findAngle(pointSX, pointSY, pointEX, pointEY):
    sign = 1
    if pointEX == pointSX:
        if pointEY > pointSY:
            return 0
        return -3*math.pi/2
    if pointEY == pointSY :
         if pointEX > pointSX:
             return math.pi/2
         return  -math.pi/2
    if pointEY > pointSY :
        return math.asin((pointEX-pointSX)/(math.sqrt((pointEY-pointSY)*(pointEY-pointSY)+(pointEX-pointSX)*(pointEX-pointSX))))
    if pointEX < pointSX:
        sign = -1
    return sign * math.asin((pointSY-pointEY)/(math.sqrt((pointEY-pointSY)*(pointEY-pointSY)+(pointEX-pointSX)*(pointEX-pointSX)))) + sign*math.pi/2


def moveForward(dis, whB, prevSt,x,y):
    xx,yy,dd =computeCoords(whB,prevSt,dis,0)
    x += xx
    y += yy
    t = requests.get("https://rover.codingcontest.org/rover/move/"+uuid+"?distance="+str(dis)+"&steeringAngle=0").text
    if dis > 0:
        print(t,x,y,prevSt)
        print(requests.get("https://rover.codingcontest.org/rover/sensor/"+uuid).text)
    return x,y

def turnToAngle(angle, whB, maxSt, prevSt, x,y):
    radius = whB / math.sin(math.radians(abs(maxSt)))
    st= 1
    if angle < 0:
        st = -1
    if abs(angle) >= 180:
        angle -= st*360
    if angle < 0:
        st = -1
    else:
        st = 1
    sensors = refreshSensors()
    while abs(angle) > 8 :
        while sensors[6] < 2 or sensors[7]<3 or sensors[8]<2:
            x,y = moveForward(-0.5,whB,prevSt,x,y)
            sensors = refreshSensors()
        dis = math.radians(4)*radius
        xx,yy,dd = computeCoords(whB,prevSt,dis,maxSt*st)
        distance = math.sqrt(xx*xx+yy*yy)
        x += xx
        y += yy
        prevSt += dd
        if prevSt >= 360:
            prevSt %= 360
        requests.get("https://rover.codingcontest.org/rover/move/"+uuid+"?distance="+str(dis)+"&steeringAngle="+str(maxSt*st))
        xx,yy,dd = computeCoords(whB,prevSt,-dis,maxSt*st*-1)
        x += xx
        y += yy
        prevSt += dd
        if prevSt >= 360:
            prevSt %= 360
        requests.get("https://rover.codingcontest.org/rover/move/"+uuid+"?distance="+str(-dis)+"&steeringAngle="+str(maxSt*st*-1))
        angle -= 8*st
    sensors =refreshSensors()
    while sensors[6] < 2 or sensors[7]<3 or sensors[8]<2:
        x,y = moveForward(-0.3,whB,prevSt,x,y)
        sensors =refreshSensors()
    dis = math.radians(abs(angle/2))*radius

    xx,yy,dd = computeCoords(whB,prevSt,dis,maxSt*st)
    x += xx
    y += yy
    prevSt += dd
    if prevSt >= 360:
        prevSt %= 360
    requests.get("https://rover.codingcontest.org/rover/move/"+uuid+"?distance="+str(dis)+"&steeringAngle="+str(maxSt*st))
    xx,yy,dd = computeCoords(whB,prevSt,-dis,maxSt*st*-1)
    x += xx
    y += yy
    prevSt += dd
    if prevSt >= 360:
        prevSt %= 360
    requests.get("https://rover.codingcontest.org/rover/move/"+uuid+"?distance="+str(-dis)+"&steeringAngle="+str(maxSt*st*-1))
    print(requests.get("https://rover.codingcontest.org/rover/sensor/"+uuid).text)

    return x,y,prevSt

def refreshSensors():
    s= requests.get("https://rover.codingcontest.org/rover/sensor/"+uuid)
    s = s.text.split(" ")
    sensors = []
    for i in range (len(s)):
        sensors.append(float(s[i]))
    return sensors

finalX =0
finalY = 0
prevSteering = 0.00
response = requests.get("https://rover.codingcontest.org/rover/create?map=L7_M6DA04KF&username=De-nix&contestId=practice")
uuid = response.text
response2= requests.get("https://rover.codingcontest.org/rover/"+uuid)
info = response2.text.split(" ")
print(info)
wheelBase = float(info[0])
maxSteering = float(info[1])
targetX = float(info[2])
targetY = float(info[3])
targetRadius = float(info[4])
angle = 0
print(refreshSensors())


while abs(finalX - targetX) + abs(finalY-targetY) > targetRadius:
    angle = math.degrees(findAngle(finalX,finalY,targetX,targetY))
    if angle < 0.0:
        angle = 360 + angle
    angle = angle - prevSteering
    finalX,finalY,prevSteering = turnToAngle(angle,wheelBase,maxSteering,prevSteering,finalX,finalY)
    sensors = refreshSensors()
    if sensors[7] > 7 :
        finalX,finalY= moveForward(1,wheelBase,prevSteering,finalX,finalY)
    sensors = refreshSensors()
    if sensors[7] < 2 :
        finalX,finalY = moveForward(-0.5,wheelBase,prevSteering,finalX,finalY)
        sensors = refreshSensors()
    if sensors[7] > 10 :
        finalX,finalY= moveForward(min(100.0,min(sensors[7]-7, math.sqrt((finalX-targetX)*(finalX-targetX)+ (finalY-targetY)*(finalY-targetY)))),wheelBase,prevSteering,finalX,finalY)
    else:
        finalX,finalY= moveForward(0.2,wheelBase,prevSteering,finalX,finalY)
        finalX,finalY,prevSteering = turnToAngle(16,wheelBase,maxSteering,prevSteering,finalX,finalY)
    sensors = refreshSensors()
    dg = math.degrees(findAngle(finalX,finalY,targetX,targetY))
    if dg < 0 :
        dg = 360+ dg
    dg = dg - prevSteering
    print ("dg ", dg, " a ",round(dg//7.33)+7)
    tr = 0
    oldX = finalX
    while abs(oldX-finalX)>5 or not (abs(dg) < 55 and sensors[round(dg//7.33)+7]>15):

        if sensors[7] < 2:
            finalX,finalY = moveForward(-0.5,wheelBase,prevSteering,finalX,finalY)
            sensors = refreshSensors()
        while sensors[6] > 15 and sensors[5] > 3:
            # if (sensors[7]>10):
            #     finalX,finalY = moveForward(1,wheelBase,prevSteering,finalX,finalY)
            finalX,finalY,prevSteering = turnToAngle(-8,wheelBase,maxSteering,prevSteering,finalX,finalY)
            sensors = refreshSensors()
        if sensors[7] > 9 and sensors[6] > 2.5:
            finalX,finalY = moveForward(5,wheelBase,prevSteering,finalX,finalY)
        else:
            finalX,finalY,prevSteering = turnToAngle(8,wheelBase,maxSteering,prevSteering,finalX,finalY)
        sensors = refreshSensors()
        print(requests.get("https://rover.codingcontest.org/rover/sensor/"+uuid).text,finalX,finalY,prevSteering)
        dg = math.degrees(findAngle(finalX,finalY,targetX,targetY))
        if dg < 0 :
            dg = 360+ dg
        dg = dg - prevSteering
        if round(dg//7.33)+7 > 0 and round(dg//7.33)+7 < 15:
            print("meters till d wall ", sensors[round(dg//7.33)+7])
