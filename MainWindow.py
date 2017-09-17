import sys, os
from PyQt5 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import FigureManagerQT
import numpy as np
import matplotlib.pyplot as plt
from SlicerCanvas import SlicerFigureCanvas
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets
from formular import Ui_MainWindow
import scipy as sc
import scipy.interpolate
import pandas as pd
import PyQt5.QtCore as QtCore


class mainwindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        #Matplotlib
        self.canvas = None
        self.fig = None
        super().__init__()
        self.setupUi(self)
        #Titel
        self.setWindowTitle('Auswertung')
        #Figure
        self.fig = Figure()
        #Setup Canvas
        self.setupCanvas()
        # List
        l = ('Schnitt', 'Linker Rand', 'Linker Graben', 'Mitte', 'Rechter Graben', 'Rechter Rand')
        self.data_table_x = pd.DataFrame(columns=l)
        self.data_table_y = pd.DataFrame(columns=l)


        #Connect
        self.ladenpushButton.pressed.connect(self.on_laden)
        self.width2Slider.valueChanged.connect(self.canvas.setFilterWidth2)
        self.width2Slider.valueChanged.connect(self.updateLW2)
        self.width3Slider.valueChanged.connect(self.updateLW3)
        self.order2Slider.valueChanged.connect(self.updateLO2)
        self.order3Slider.valueChanged.connect(self.updateLO3)
        self.order2Slider.valueChanged.connect(self.canvas.setFilterOrder2)
        self.width3Slider.valueChanged.connect(self.canvas.setFilterWidth3)
        self.order3Slider.valueChanged.connect(self.canvas.setFilterOrder3)
        self.addpushButton.pressed.connect(self.on_add)
        self.savepushButton.pressed.connect(self.on_save)

    def on_save(self):
        fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Speichere Datensatz', '~/Dokumente/GitHub')

        ew = pd.ExcelWriter(fname[0]+'.xlsx')
        self.data_table_x.to_excel(ew, 'X Schnitt')
        self.data_table_y.to_excel(ew, 'Y Schnitt')
        ew.save()
        ew.close()

    def on_add(self):
        xschnitt = self.canvas.rowplot
        yschnitt = self.canvas.colplot
        la, lg, m, rg, rr = self.canvas.maximar[0],self.canvas.maximar[1],self.canvas.maximar[2],self.canvas.maximar[3],self.canvas.maximar[4]
        data = [xschnitt, la, lg, m, rg, rr]
        self.data_table_x.loc[len(self.data_table_x)] = data
        la, lg, m, rg, rr = self.canvas.maximac[0], self.canvas.maximac[1], self.canvas.maximac[2], self.canvas.maximac[3], self.canvas.maximac[4]
        data = [yschnitt, la, lg, m, rg, rr]
        self.data_table_y.loc[len(self.data_table_y)] = data
        print(self.data_table_x)


    def updateLW2(self, m):
        self.labelWidth2.setText(str(m))

    def updateLW3(self, m):
        self.labelWidth3.setText(str(m))

    def updateLO2(self, m):
        self.labelOrder2.setText(str(m))

    def updateLO3(self, m):
        self.labelOrder3.setText(str(m))

    def keyPressEvent(self, event):
        super(mainwindow, self).keyPressEvent(event)
        event.accept()
        if event.key() == QtCore.Qt.Key_X:
            self.canvas.plotRow(self.canvas.rowplot)
            self.canvas.plotCol(self.canvas.colplot)
            self.canvas.update()
            self.canvas.draw()
            self.canvas.refreshSanchezArtists()
            self.canvas.cancelPlot()
        elif event.key() == QtCore.Qt.Key_C:
            self.canvas.reconnectPlot()

    def on_laden(self):
        spaltenn = (
            "Linker Rand X", "Linker Rand Y", "Linker Graben X", "Linker Graben X", "Mitte X", "Mitte Y",
            "Rechter Graben X",
            "Rechter Graben Y", "Rechter Graben X", "Rechter Graben Y")
        dx = pd.DataFrame(columns=spaltenn)
        dy = pd.DataFrame(columns=spaltenn)

        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Öffne Datei', '/home/sebastian/Dokumente/GitH/Spotauswertung/Spotauswertung')
        searchfile = None

        if fname[0]:
            searchfile = open(fname[0], "r")
        else:
            return
        """
        Nach Ende des Header suchen
        """

        linenumber = 0
        headerend = None
        fileend = None
        for line in searchfile:
            linenumber += 1
            if line.find('#') is not -1 and headerend is None:
                headerend = linenumber

            if line.find('#') is not -1 and headerend is not None:
                fileend = linenumber

        searchfile.close()
        # Damit ist bekannt, wie lange der Header ist, beginnend bei Null

        rdata = pd.read_table(fname[0], header=headerend, nrows=fileend - headerend - 2, sep="\s+")
        del rdata[rdata.columns[-1]]
        rdata.columns = ["X", "Y", "Z"]
        rdata = rdata.replace(to_replace={"Z" : {"No" : 0}})
        rdata = rdata.convert_objects(convert_numeric=True)

        x = rdata["X"].as_matrix()
        y = rdata["Y"].as_matrix()
        z = rdata["Z"].as_matrix()

        n = len(x)
        x1, y1 = np.linspace(x.min(), x.max(), 1000), np.linspace(y.min(), y.max(), 1000)
        X, Y = np.meshgrid(x1, y1)

        Z = sc.interpolate.griddata((x.flatten(), y.flatten()), z.flatten(), (X, Y),
                                    method='nearest')  # flatten wird benutzt, um daraus ein 1D-Array zu machen
        Z = np.abs(Z)
        Z[np.isnan(Z)] = 0
        Z = Z - Z.min()
        self.Z = Z
        self.canvas.Z = Z
        self.canvas.replot()

    def on_keyboard(self, event):
        print(event.accept())

    def setupCanvas(self):
        self.canvas = SlicerFigureCanvas()
        self.Container.addWidget(self.canvas)
        self.canvas.draw()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = mainwindow()
    window.show()
    sys.exit(app.exec_())
