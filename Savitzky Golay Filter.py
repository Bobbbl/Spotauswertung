# -*- coding: utf-8 -*-
"""
Created on Sun Sep  3 08:37:50 2017

@author: Sebastian Draxinger

File testet das 
1.
Das Glätten der Schnitte aus der Spotauswertung

2.
Das legen von Punkten (Wendepunkte) auf dem Graphen
"""
import sys
from DraggableCanvas import plotDrag
import numpy as np
import scipy.io
import scipy as sc
from scipy.signal import argrelextrema
import pandas as pd
from Filter import savitzky_golay
from mpl_toolkits.mplot3d import Axes3D
from SlicerCanvas import plotSlice


import matplotlib.pyplot as plt
plt.switch_backend('Qt5Agg')

def main():
    spaltenn = (
    "Linker Rand X", "Linker Rand Y", "Linker Graben X", "Linker Graben X", "Mitte X", "Mitte Y", "Rechter Graben X",
    "Rechter Graben Y", "Rechter Graben X", "Rechter Graben Y")
    dx = pd.DataFrame(columns=spaltenn)
    dy = pd.DataFrame(columns=spaltenn)

    """
    Nach Ende des Header suchen
    """
    searchfile = open("Mask.txt", "r")
    linenumber = 0
    headerend = None
    fileend = None
    for line in searchfile:
        linenumber += 1
        if line.find('#') is not -1 and headerend is None:
            headerend = linenumber

        if line.find('#') is not -1 and headerend is not None:
            fileend = linenumber

    # Damit ist bekannt, wie lange der Header ist, beginnend bei Null

    rdata = pd.read_table("Mask.txt", header=headerend, nrows=fileend - headerend - 2, sep="\s+")
    del rdata[rdata.columns[-1]]
    rdata.columns = ["X","Y","Z"]
    rdata["Z"] = rdata["Z"].map({"No" : np.NaN})

    mat1    =   scipy.io.loadmat("S1.mat")
    mat19   =   scipy.io.loadmat("S19.mat")


    x, y, z = mat19['X'], mat19["Y"], mat19["Z"]

    #x = rdata["X"].as_matrix()
    #y = rdata["Y"].as_matrix()
    #z = rdata["Z"].as_matrix()

    n = len(x)
    x1,y1 = np.linspace(x.min(),x.max(), 50),np.linspace(y.min(),y.max(), 50)
    X,Y = np.meshgrid(x1,y1)
    print('meshgrid successfull')

    Z = sc.interpolate.griddata ((x.flatten(),y.flatten()), z.flatten(), (X,Y), method='nearest') #flatten wird benutzt, um daraus ein 1D-Array zu machen
    Z = np.abs(Z)
    Z[np.isnan(Z)] = 0
    Z = Z - Z.min()
    #Z[Z<0] = 0


    xschnitt = Z[25,:]
    yschnitt = Z[:,25]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    orLine = ax.plot(xschnitt)
    #ax = Axes3D(fig)
    #ax.scatter(x, y, z)
    #plt.show()
    plotSlice(Z)




    window_size = 7
    order = 1
    fline = ax.plot(np.linspace(xschnitt.max(),xschnitt.max(),len(xschnitt)))
    xfschnitt = []
    jumpx = False
    jumpy = False

    while window_size != 0:

        plt.pause(0.1)

        window_size = int(input("X::Nummer für Filterbreite und 0 um fortzufahren: "))
        order = int(input("X::Nummer für Order und 0 um fortzufahren: "))

        if(window_size == 222):
            xfschnitt = np.linspace(0, 0, xfschnitt.size)
            jumpx = True
            break
        if(window_size == 0):
            break

        xfschnitt = savitzky_golay(xschnitt, window_size, order)

        fline[0].set_ydata(xfschnitt)
        fig.canvas.draw()



    window_size = 7
    order = 1
    yfschnitt = []
    fline[0].remove()
    orLine[0].remove()
    orLine = ax.plot(yschnitt)
    fline = ax.plot(np.linspace(yschnitt.max(), yschnitt.max(), len(yschnitt)))
    fig.canvas.draw()

    while window_size != 0:

        plt.pause(0.1)

        window_size = int(input("Y::Nummer für Filterbreite und 0 um fortzufahren: "))
        order = int(input("Y::Nummer für Order und 0 um fortzufahren: "))

        if window_size == 222:
            xfschnitt = np.linspace(0, 0, xfschnitt.size)
            jumpy = True
            break
        if window_size == 0:
            break

        yfschnitt = savitzky_golay(yschnitt, window_size, order)

        fline[0].set_ydata(yfschnitt)
        fig.canvas.draw()








    plt.close(fig)
    """
    Wichtigen Punkte bestimmen
    Zunächst die Wölbungen
    """
    a = xfschnitt[0]
    ran = xfschnitt.min()/100 * 10
    # for local maxima
    maxima = argrelextrema(xfschnitt, np.greater, order=20)
    minima = argrelextrema(xfschnitt, np.less, order=20)


    """
    Wendepunkte plotten mit eigener Canvas
    Die Wendepunkte sind markiert und können 
    verschoben werden
    """
    if not jumpx:
        data = plotDrag(xfschnitt, np.hstack([maxima[0], minima[0], 0, len(xfschnitt)-1]))
        if data[0].shape[0] is not 5:
            print("Schlechte Datenqualität\n" + "Daten werden gelöscht")
            data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        else:
            data = [data[0][0], data[1][0], data[0][1], data[1][1], data[0][2], data[1][2], data[0][3], data[1][3], data[0][4], data[1][4]]
    else:
        data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        jumpx = False

    dx.loc[len(dx)] = data

    if not jumpy:
        data = plotDrag(yfschnitt, np.hstack([maxima[0], minima[0], 0, len(yfschnitt)-1]))
        if data[0].shape[0] is not 5:
            print("Schlechte Datenqualität\n" + "Daten werden gelöscht")
            data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        else:
            data = [data[0][0], data[1][0], data[0][1], data[1][1], data[0][2], data[1][2], data[0][3], data[1][3], data[0][4], data[1][4]]
    else:
        data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        jumpy = False

    dy.loc[len(dy)] = data

if __name__ == '__main__':

    main()

    sys.exit(0)

