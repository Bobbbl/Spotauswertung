# -*- coding: utf-8 -*-
"""
Spyder Editor

Das ist ein Versuch, um zu überprüfen wie A:
    Convolution zusammen mit Python/Scipy funktioniert
und B:
    Ob diese "Zitterer" wirklich einen Einfluss auf die 
    Auswertung haben

"""
#Import Scipy
import scipy as sc
import scipy.io
import scipy.signal
import numpy as np
import math
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm

#Load Spot
mat1 = scipy.io.loadmat('S1.mat')
mat19 = scipy.io.loadmat('S19.mat')


x, y, z = mat19['X'], mat19['Y'], mat19['Z']
n = len(x)
x1,y1 = np.linspace(x.min(),x.max(), 50),np.linspace(y.min(),y.max(), 50)
X,Y = np.meshgrid(x1,y1)
print('meshgrid successfull')

Z = sc.interpolate.griddata((x.flatten(),y.flatten()), z.flatten(), (X,Y), method='nearest') #flatten wird benutzt, um daraus ein 1D-Array zu machen
Z = Z - Z.min()
Z[Z<0] = 0
print('Interpolation successfull')

#Convolution
map2d = np.zeros((50,2000))
map2d[math.floor(map2d.shape[0]/2), :] = -0.05;
cmat = scipy.signal.convolve2d(map2d, Z, mode='full')
print('Convolution successfull')

#Plot Spot
fig = plt.figure()
ax2 = fig.add_subplot(111, projection='3d')
x1,y1 = np.linspace(x.min(),x.max(), cmat.shape[1]),np.linspace(y.min(),y.max(), cmat.shape[0])
Xc,Yc = np.meshgrid(x1,y1)
cmat[cmat==0] = np.NaN
ax2.plot_surface(Xc,Yc,cmat,cmap=cm.coolwarm, linewidth=0)
plt.show()


