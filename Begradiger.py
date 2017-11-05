from PyQt5 import QtWidgets
from matplotlib.figure import Figure
import sys
import matplotlib
import numpy as np
from GeradenpunkteCanvas import GeradenpunkteCanvas
from FormularBegradigen import Ui_Form
import scipy
import pandas as pd
import PyQt5.QtCore as QtCore
import os
import copy

matplotlib.use('Qt5Agg')


class Begradiger(QtWidgets.QWidget, Ui_Form):

    def __init__(self):
        self.canvas = None
        self.fig = None
        super().__init__()
        self.setupUi(self)


        # Setup Canvas
        self.canvas = GeradenpunkteCanvas()
        self.Container.addWidget(self.canvas)
        self.canvas.draw()

        # Connect
        self.pushButtonLaden.pressed.connect(self.laden)
        self.listWidget.currentItemChanged.connect(self.on_item_changed)

        # Count
        self.count = 0

        self.itemlist = []
        self.spotxdic = {}
        self.spotydic = {}
        self.currentSpotx = None
        self.currentSpoty = None

    def laden(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Öffne Datei',
                                                      os.path.abspath(os.getcwd()))
        efile = pd.read_excel(fname[0], sheetname=None)
        self.addListElements(self.count, efile)
        self.count = self.count + 9

    def addListElements(self, num, table):
        ranger = 0
        for i in range(num, num+9):
            self.listWidget.addItem('%s' % (i+1))
            self.addElementToItemList(i, ranger, table)
            ranger = ranger + 1

    def addElementToItemList(self, i, num, table):
        sheetx = table['X Schnitt Realgrö0e']
        sheety = table['Y Schnitt Realgrö0e']
        spotx  = sheetx.loc[num]
        spoty = sheety.loc[num]
        self.spotxdic['%s' % i] = spotx
        self.spotydic['%s' % i] = spoty




    def on_item_changed(self, curr, prev):
        self.currentSpotx = self.spotxdic[str(int(curr.text())-1)]
        self.currentSpoty = self.spotydic[str(int(curr.text())-1)]
        x = self.extractXfS(self.currentSpotx)
        y = self.extractYfS(self.currentSpotx)
        px = self.extractPixelsizefS(self.currentSpotx)
        self.canvas.plot(x,y)

    def extractXfS(self, spot):
        return [spot[1], spot[3], spot[5], spot[7],spot[9]]

    def extractYfS(self, spot):
        return [spot[2], spot[4], spot[6], spot[8],spot[10]]

    def extractPixelsizefS(self, spot):
        return spot[11]

