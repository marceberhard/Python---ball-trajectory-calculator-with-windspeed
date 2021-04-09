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
timeSteps = 100
timeMin = 0

def basicCalculations(angleDegrees):
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
    #print(res)
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

def realerWurf(speed, angle, windSpeed):
    global v0
    global wind
    wind = windSpeed
    angleDegrees = angle
    v0 = speed
    basicCalculations(angleDegrees)
    wWind = solverThrowWithWind(v0, angleB)
    widthRes = wWind[1].max()
    heightRes = wWind[2].max()
    widthRes = round(widthRes, 2)
    heightRes = round(heightRes, 2)
    print("=================>  Length with Wind Resistance " + str(widthRes) + "m  <=================")
    print("=================>  Height with Wind Resistance " + str(heightRes) + "m  <=================")
    printGraf(wWind[1], wWind[2])
    diff = widthRes-83.41 #hardcoded due to const values & performance - according to exercise 3
    diff = round(diff, 2)
    print("Distance difference (10m/s wind distance value subtracted) is about: " + str(diff) + "m")


realerWurf(30, 45, -10) #realerWurf (v0, phi, wind) - negativ value represents opposite wind direction
print("**************************     WITHOUT WIND     **************************") #enter only v0 and angle values for calculation
realerWurf(30, 45, 0)
sys.exit()
