import sys
from PyQt5 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import FigureManagerQT
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.spatial.distance import euclidean

class GeradenpunkteCanvas(FigureCanvasQTAgg):

    def __init__(self):
        self.figure = Figure()
        super(GeradenpunkteCanvas, self).__init__(self.figure)

        # Background - Damit nicht jedes Mal der gesamte Plot
        # wiederholt werden muss
        self.background = None

        # Die Koordinaten, die der User später auslesen kann,
        # wenn er Lust hat
        self.x = None
        self.y = None
        self.xnew = None
        self.ynew = None

        # Connect - Das Connecten bei der Klasse von Matplotlib
        # läuft etwas anders als bei den klassischen Klassen von
        # Qt

        # Setup Ax
        self.ax = self.figure.add_subplot(111)

        # Setup Interpolate Line
        x, y = self.interpolate([0,1,2,3,4], [0,0,0,0,0])
        self.iline = self.ax.plot(x, y)
        self.ix = x
        self.iy = y

        # Setup Scatter Line
        self.x = [0,1,2,3,4]
        self.y = [0,0,0,0,0]
        self.line = self.ax.plot(self.x, self.y, marker='o', linestyle='None', color='r')

        # Calculate Corrected Points
        xn, yn = self.calcNewCoordinates(x, y)
        self.cx, self.cy = xn, yn
        # Plot Corrected Points
        self.cline = self.ax.plot(self.cx, self.cy, marker='.', linestyle='None', color='g')

    def plot(self, x, y):
        # Plot Data Points
        self.line[0].set_xdata(x)
        self.line[0].set_ydata(y)
        self.x = x
        self.y = y
        # Interpolate Line Data
        ix, iy = self.interpolate(x,y)
        self.ix = ix
        self.iy = iy
        # Plot Interpolated Line Data
        self.iline[0].set_ydata(iy)
        self.iline[0].set_xdata(ix)
        # Calculate Corrected Points
        xn, yn = self.calcNewCoordinates(x, y)
        self.cx, self.cy = xn, yn
        # Plot Corrected Points
        self.cline[0].set_ydata(yn)
        self.cline[0].set_xdata(xn)
        #Recalculate Limits
        self.ax.relim()
        self.ax.autoscale_view(True, True, True)
        # Redraw
        self.draw()

    def interpolate(self, x, y):
        f = interp1d([x[0], x[-1]],[y[0], y[-1]], kind='linear')
        ynew = f(x)
        return x, ynew

    def calcNewCoordinates(self, x, y):
        # Sehen, in welche Richtung die Gerade
        # geneigt ist und dementsprechend die
        # Anfangskoordinate auswählen
        yanfang = None
        xanfang = None
        yende = None
        xende = None
        if y[0] > y[-1]:
            yanfang = y[-1]
            xanfang = x[-1]

            yende = y[0]
            xende = x[0]
        else:
            yanfang = y[0]
            xanfang = x[0]

            yende = y[-1]
            xende = x[-1]
        # Ortsvektor von Anfang und Ende
        apkt = np.array([xanfang, yanfang])
        epkt = np.array([xende, yende])
        # Ortsvektor von Hypothenuse
        hyp = apkt + epkt - apkt
        # Länge Hypthenuse
        lhyp = np.linalg.norm(hyp)
        # Länge Ankathete
        lank = np.abs(xende - xanfang)
        # Länge Gegenkathete
        lgeg = yende - yanfang #Gleichzeitig auch der erste korrigierte Wert
        # Alpha
        alpha = np.arcsin(lgeg/lhyp)
        # YNEW - Neue Koordinaten
        ynew = []
        yn = None
        for i in range(len(y)):
            dis = yende - self.iy[i]
            ynew.append(self.y[i]+dis)

        return x, ynew



