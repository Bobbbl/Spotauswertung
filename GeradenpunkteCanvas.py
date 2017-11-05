import sys
from PyQt5 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import FigureManagerQT
import numpy as np
import matplotlib.pyplot as plt

class GeradenpunkteCanvas(FigureCanvasQTAgg):

    def __init__(self):
        self.figure = Figure()
        super(GeradenpunkteCanvas, self).__init__(self.figure)

        # Background - Damit nicht jedes Mal der gesamte Plot
        # wiederholt werden muss
        self.background = None

        # Connect - Das Connecten bei der Klasse von Matplotlib
        # läuft etwas anders als bei den klassischen Klassen von
        # Qt

        # Setup Ax
        self.ax = self.figure.add_subplot(111)

        # Setup Scatter Line
        self.line = self.ax.plot([0,1,2,3,4], [0,0,0,0,0], marker='o', linestyle='None')

    def plot(self, x, y):
        self.line[0].set_xdata(x)
        self.line[0].set_ydata(y)
        self.ax.relim()
        self.ax.autoscale_view(True, True, True)
        self.draw()





