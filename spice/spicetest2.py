# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 19:00:55 2021

@author: frank
"""
import numpy as np
from matplotlib import pylab as plt

"""
# Vert
# 150k to 250k
R5 = 200000
C1 = 0.1e-6

R3 = 2000
R4 = 2000

R6 = 220000
C2 = 0.2e-6

R1 = 2000
R2 = 2000
"""


# Horiz
# 150k to 250k
R5 = 200000
C1 = 390e-12

R3 = 2000
R4 = 2000

R6 = 220000
C2 = 330e-12

R1 = 2000
R2 = 2000


Vcc = 6.0
Vt = 0.65

def calcDelta(R,C,Vcc,Vt):
    tau = R*C
    dt = tau*(np.log(2*Vcc-Vt)-np.log(Vcc-Vt))
    return dt

t = np.arange(0,20.0e-3,0.1e-3)
tau = R1*C1
K = Vt-2*Vcc
y = Vcc+K*np.exp(-t/(tau))
tau2 = R2*C2
K2 = 2*Vcc-Vt
y2 = K2*np.exp(-t/(tau2))

dt1 = calcDelta(R5,C1,Vcc,Vt)
print(dt1)
dt2 = calcDelta(R6,C2,Vcc,Vt)
print(dt2)
if dt1 < dt2:
    offtime = dt1
else:
    offtime = dt2
print(offtime)

# looks like 2.25 taus to discharge
dt3 = 2.25*(R3+R4)*C1
dt4 = 2.25*(R1+R2)*C2

if dt3 < dt4:
    ontime = dt3
else:
    ontime = dt4

print(ontime, offtime, ontime+offtime)
print(1.0/(ontime+offtime))

plt.plot(t,y,t,y2)
plt.grid(True)
plt.show()


