import time
import numpy as np
import math
from matplotlib import pyplot as plt

f1 = open('flightdata/flightData-2021-05-01T12-28-51.968158.txt','r')
f2 = open('flightdata/flightData-2021-05-01T11-19-59.374263.txt','r')

#eeeeeeeeeeee
GaltP = []
GvGPS = []
GvPalt = []
#prealloc
AaltP = []
AvGPS = []
AvPalt = []

#Barometric Equations:
def press_alt(P):
    gOxM = 0.284044 # (m*kg)/(s^2*mol)
    R = 8.3144598 # J/(mol*K)
    Tb = 273.15 #K
    hb = 0 #m
    Pb = 101325 #Pa
    #global initializing
    #global Pb
    #global Tb
    #if initializing > 0:
    #   temps.append(data.temp + 273.15)
    #   pressures.append(data.pressure)
    #   Tb = sum(temps) / len(temps)
    #   Pb = sum(pressures) / len(pressures)
    #   initializing -= 1
    if (22632.1 < P <= 101325):
        lapse = -0.0065
    elif (5474.89 <= P < 22632.1):
        lapse = 0
    elif (868.02 <= P < 5474.89):
        lapse = 0.001
    elif (110.91 <= P < 868.02):
        lapse = 0.0028
    else:
        lapse = 0
    if lapse != 0:
        h = hb + (Tb/lapse)*((math.pow((P/Pb),((-1*R*lapse)/gOxM))-1))
        #(((((math.log(data.pressure/Pb))/math.log((-1*gOxM)/(lapse*R)))-1)*Tb)/lapse + hb)
        if P <= 0:
            h = 0
    elif lapse == 0:
        if P <= 0:
            h = 0
        else:
            h = (hb-R*Tb*math.log(P)/((gOxM)*math.log(Pb)))
    return h


#file reading and naming
raw1 = f1.readlines()
raw2 = f2.readlines()

data1 = np.matrix([[float(x) for x in line[:-1].split(' ')] for line in raw1])
data2 = np.matrix([[float(x) for x in line[:-1].split(' ')] for line in raw2])

#Ground
#Altitudes
GaltGPS = data1[:,4]
GPressures = data1[:,11]
for pressure in GPressures:
    GaltP.append(press_alt(pressure))
#Time
GadjustTime = data1[:,1]/1000
#Average Velocity
for i in range(len(GaltGPS)-1):
    GvGPS.append((GaltGPS[i+1] - GaltGPS[i])/(GadjustTime[i+1] - GadjustTime[i]))
    GvPalt.append((GaltP[i+1] - GaltP[i])/(GadjustTime[i+1] - GadjustTime[i]))
#3space GPS
Glat = data1[:,2]
Glon = data1[:,3]

#plotting
plt.title("Altitude vs Time")
plt.xlabel("Time [s]")
plt.ylabel("Altitude [m]")
ax = plt.gca()
ax.set_xlim(min(GadjustTime),max(GadjustTime))
ax.set_ylim(min(GaltP),max(GaltP))
plt.plot(GadjustTime.A1,np.array(GaltGPS))
plt.plot(GadjustTime.A1,np.array(GaltP))
plt.show()

#Raspberry Pi
#Barometric Equations:

#Altitudes
AaltGPS = data2[:,4]
APressures = data2[:,11]
for pressure in APressures:
    AaltP.append(press_alt(pressure))
#Time
AadjustTime = data2[:,1]/1000
#Average Velocity
for i in range(len(AaltGPS.A1)-1):
    AvGPS.append((AaltGPS.A1[i+1] - AaltGPS.A1[i])/(AadjustTime.A1[i+1] - AadjustTime.A1[i]))
    AvPalt.append((AaltP[i+1] - AaltP[i])/(AadjustTime.A1[i+1] - AadjustTime.A1[i]))
#3space GPS
Alat = data2[:,2]
Alon = data2[:,3]

#Pi plotting
plt.title("Altitude vs Time")
plt.xlabel("Time [s]")
plt.ylabel("Altitude [m]")
ax = plt.gca()
ax.set_xlim(min(AadjustTime),max(AadjustTime))
ax.set_ylim(min(AaltP),max(AaltP))
plt.plot(AadjustTime.A1,np.array(AaltGPS))
plt.plot(AadjustTime.A1,np.array(AaltP))
plt.show()

# Barometric Velocity
plt.title("Velocity vs Time")
plt.xlabel("Time [s]")
plt.ylabel("Velocity [m/s]")
ax = plt.gca()
ax.set_xlim(min(AadjustTime),max(AadjustTime))
ax.set_ylim(min(AvPalt),max(AvPalt))
#plt.plot(AadjustTime.A1[:-1],AvGPS)
plt.plot(AadjustTime.A1[:-1],AvPalt)
plt.show()
