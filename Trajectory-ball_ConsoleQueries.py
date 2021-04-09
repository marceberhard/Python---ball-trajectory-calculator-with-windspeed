import math
import matplotlib.pyplot as plt
import matplotlib.animation as ani
from scipy.integrate import solve_ivp
import sys
import numpy as np
np.set_printoptions(suppress=True)
fig, ax = plt.subplots()

#Value Initialization
global angleDegrees
angleDegrees = 0 #degreesQueried@Entry
rhoA = 1.2 #Density air
Cwa = 0.45 #Resistance air
rK = 0.08 #Radius uf ball in m
rhoK = 2700 #Density of ball
flK = 0 #surface ball
g = 9.81 #gravitation
timeSteps = 100 #for plot
timeMin = 0

def queryAngle():
    while True:
        angleDegrees = float(input("Please enter angle in degrees: "))
        try:
            angleDegrees = int(angleDegrees)
            return angleDegrees
            if (0 < angleDegrees < 90):
                break
            else:
                print("False Entry - Retry")
                continue
        except:
            print("Not possible entry - retry")

def v0Query():
    v0 = float(input("Please enter departure velocity in m/s: "))
    try:
        v0 = int(v0)
        return v0

    except:
        print("Not possible entry - retry")

def windQuery():
    wind = float(input("Please enter wind coming in x direction (-values for facing against direction of throw) "))
    try:
        wind = int(wind)
        return wind

    except:
        print("Not possible entry - retry")

def basicCalculations():
    vK = (4/3)*np.pi*(rK*rK*rK)
    mK = vK* rhoK
    global angleB
    angleB = angleDegrees * np.pi / 180
    flK = np.pi*rK**2
    global K
    K = (Cwa*rhoA*flK)/(2 * mK)
    global timeMax
    timeMax = 2*v0*math.sin(angleB)/g
    global v0x
    global v0y
    v0x = v0 * math.cos(angleB)
    v0y = v0 * math.sin(angleB)

def printGraf(arr1, arr2):
    plt.figure(1, figsize=(10, 8))
    plt.title('Toss parable with wind resistance')
    plt.xlabel('x')
    plt.ylabel('y(x)')
    plt.grid()
    plt.plot(arr1, arr2,'-')
    plt.ylim(bottom=0)
    plt.show()

def solverThrowWithWind(v, aBPhi):
    timeMax = 2 * v * math.sin(aBPhi) / g
    y = [0, v0x, 0, v0y]
    res = solve_ivp(compderiv, (0, timeMax), y, first_step=0.1, max_step=0.1)
    return [res.t, res.y[0], res.y[2]]

def compderiv(t, y ):
  nf = len(y)
  dy = np.zeros(nf)
  totvel = np.sqrt((y[1] - wind)**2 + y[3]**2)
  dy[0] = y[1]
  dy[1] = - K*totvel*(y[1]-wind)
  dy[2] = y[3]
  dy[3] = - g - K*totvel*y[3]
  return dy

b = int(input("Press: '0' for specific params.   |||   Enter '1' for Demo (wind: -10m/s, speed:30m/s, angle: 45Degrees) |||  Enter '2' for Demo (wind: 0m/s, speed:30m/s, angle: 45Degrees)"))
if (b==1):
    angleDegrees = 45
    v0 = 30
    wind = -10
    basicCalculations()
    wWind = solverThrowWithWind(v0, angleB)
    widthRes = wWind[1].max()
    heightRes = wWind[2].max()
    widthRes = round(widthRes, 2)
    heightRes = round(heightRes, 2)
    print("=================>  Length with wind Resistance " + str(widthRes) + "m  <=================")
    print("=================>  Height with wind Resistance " + str(heightRes) + "m  <=================")
    printGraf(wWind[1], wWind[2])

elif (b == 2):
    angleDegrees = 45
    v0 = 30
    wind = 0
    basicCalculations()
    wWind = solverThrowWithWind(v0, angleB)
    widthRes = wWind[1].max()
    heightRes = wWind[2].max()
    widthRes = round(widthRes, 2)
    heightRes = round(heightRes, 2)
    print("=================>  Length with no extra wind Resistance " + str(widthRes) + "m  <=================")
    print("=================>  Height with no extra wind Resistance " + str(heightRes) + "m  <=================")
    printGraf(wWind[1], wWind[2])

elif (b==0):
    angleDegrees = queryAngle()
    v0 = v0Query()
    wind = windQuery()
    basicCalculations()
    wWind = solverThrowWithWind(v0, angleB)
    widthRes = wWind[1].max()
    heightRes = wWind[2].max()
    widthRes = round(widthRes, 2)
    heightRes = round(heightRes, 2)
    print("=================>  Length with Wind Resistance " + str(widthRes) + "m  <=================")
    print("=================>  Height with Wind Resistance " + str(heightRes) + "m  <=================")
    printGraf(wWind[1], wWind[2])
    diff = widthRes - 83.41 #hardcoded due to const value & performance
    diff = round(diff, 2)
    print("Distance difference (10m/s wind distance value subtracted) is about: " + str(diff) + "m")

else:
    print("Invalid Input, exiting - Restart Script and try with correct input")
    sys.exit()
