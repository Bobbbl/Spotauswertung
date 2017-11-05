# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
import Begradiger
from matplotlib.figure import Figure
import sys
import matplotlib
import numpy as np
from SlicerCanvas import SlicerFigureCanvas
from formular import Ui_MainWindow
import scipy as sc
import pandas as pd
import PyQt5.QtCore as QtCore
import Cutter
matplotlib.use('Qt5Agg')


class mainwindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        # Matplotlib
        self.canvas = None
        self.fig = None
        super().__init__()
        self.setupUi(self)
        # Titel
        self.setWindowTitle('Auswertung')
        # Figure
        self.fig = Figure()
        # Setup Canvas
        self.setupCanvas()
        self.pixelsize = None
        # List
        l = ('Schnitt Y', 'Linker Rand X',
         'Linker Rand Y',
                        'Linker Graben X',
                        'Linker Graben Y',
                        'Mitte X',
                        'Mitte Y',
                        'Rechter Graben X',
                        'Rechter Graben Y',
                        'Rechter Rand X',
                        'Rechter Rand Y')
        l_p = ('Schnitt Y',
                'Linker Rand X',
                'Linker Rand Y',
                'Linker Graben X',
                'Linker Graben Y',
                'Mitte X',
                'Mitte Y',
                'Rechter Graben X',
                'Rechter Graben Y',
                'Rechter Rand X',
                'Rechter Rand Y',
                'Pixelgröße')
        self.data_table_x = pd.DataFrame(columns=l)
        self.data_table_y = pd.DataFrame(columns=l)
        self.data_table_x_pix = pd.DataFrame(columns=l_p)
        self.data_table_y_pix = pd.DataFrame(columns=l_p)

        # self.Z_cut = None

        # Connect
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
        self.CutpushButton.pressed.connect(self.on_cut)
        # self.canvas.auswahlGetroffen.connect(self.auswahlGetroffenSlot)

    def auswahlGetroffenSlot(self):
        cutter = Cutter.Cutter(self.canvas.Z, self.canvas)

    def on_cut(self):
        self.cutter = Cutter.Cutter(self.Z, self.canvas)
        self.cutter.show()

    def on_save(self):
        fname = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Speichere Datensatz', '~/Dokumente/GitHub')

        ew = pd.ExcelWriter(fname[0] + '.xlsx')
        self.data_table_x.to_excel(ew, 'X Schnitt')
        self.data_table_y.to_excel(ew, 'Y Schnitt')
        self.data_table_x_pix.to_excel(ew, 'X Schnitt Realgrö0e')
        self.data_table_y_pix.to_excel(ew, 'Y Schnitt Realgrö0e')
        ew.save()
        ew.close()

    def on_add(self):
        xschnitt = self.canvas.rowplot
        yschnitt = self.canvas.colplot
        lax, lgx, mx, rgx, rrx, lay, lgy, my, rgy, rry = self.canvas.maximar[0], self.canvas.maximar[1],\
            self.canvas.maximar[2], self.canvas.maximar[3], self.canvas.maximar[4],\
            self.canvas.rowplot[self.canvas.maximar[0]], self.canvas.rowplot[self.canvas.maximar[1]], self.canvas.rowplot[self.canvas.maximar[2]], \
            self.canvas.rowplot[self.canvas.maximar[3]
                                ], self.canvas.rowplot[self.canvas.maximar[4]]

        data = [xschnitt, lax, lay, lgx, lgy, mx, my, rgx, rgy, rrx, rry]
        self.data_table_x.loc[len(self.data_table_x)] = data
        # ##
        data = [xschnitt, lax * self.pixelsize, lay, lgx * self.pixelsize, lgy, mx * self.pixelsize, my,
                rgx * self.pixelsize, rgy, rrx * self.pixelsize, rry, self.pixelsize]
        self.data_table_x_pix.loc[len(self.data_table_x_pix)] = data
        # ##
        lax, lgx, mx, rgx, rrx, lay, lgy, my, rgy, rry = self.canvas.maximac[0], self.canvas.maximac[1], \
            self.canvas.maximac[2], self.canvas.maximac[3], \
            self.canvas.maximac[4], \
            self.canvas.colplot[self.canvas.maximac[0]], \
            self.canvas.colplot[self.canvas.maximac[1]], \
            self.canvas.colplot[self.canvas.maximac[2]], \
            self.canvas.colplot[self.canvas.maximac[3]], \
            self.canvas.colplot[self.canvas.maximac[4]]
        data = [yschnitt, lax, lay, lgx, lgy, mx, my, rgx, rgy, rrx, rry]
        self.data_table_y.loc[len(self.data_table_y)] = data
        # By Pixel
        # X
        data = [yschnitt, lax * self.pixelsize, lay, lgx * self.pixelsize, lgy, mx *
                self.pixelsize, my, rgx * self.pixelsize, rgy, rrx * self.pixelsize, rry, self.pixelsize]
        self.data_table_y_pix.loc[len(self.data_table_y_pix)] = data

        # Debug
        print(self.data_table_x_pix)

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
        fname = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Öffne Datei',
            '/home/sebastian/Dokumente/GitH/Spotauswertung/Spotauswertung')
        searchfile = None
        # TODO: Dringend muss noch die Pixelgröße ausgelesen werden
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

            if linenumber == 8:
                tmp = line.split(' ')
                self.pixelsize = float(tmp[7 - 1])

            if line.find('#') is not -1 and headerend is None:
                headerend = linenumber

            if line.find('#') is not -1 and headerend is not None:
                fileend = linenumber

        searchfile.close()
        # Damit ist bekannt, wie lange der Header ist, beginnend bei Null

        rdata = pd.read_table(
            fname[0], header=headerend,
            nrows=fileend - headerend - 2,
            sep="\s+")

        del rdata[rdata.columns[-1]]
        rdata.columns = ["X", "Y", "Z"]
        rdata = rdata.replace(to_replace={"Z": {"No": np.NaN}})
        rdata = rdata.convert_objects(convert_numeric=True)

        x = rdata["X"].as_matrix()
        y = rdata["Y"].as_matrix()
        z = rdata["Z"].as_matrix()

        x1, y1 = np.linspace(x.min(), x.max(), 1000), np.linspace(
            y.min(), y.max(), 1000)
        X, Y = np.meshgrid(x1, y1)

        Z = sc.interpolate.griddata((x.flatten(), y.flatten()), z.flatten(), (X, Y),
                                    method='nearest')  # flatten wird benutzt, 
                                                       # um daraus ein 1D-Array zu machen
        self.Z = Z
        self.canvas.Z_cut = Z
        self.canvas.Z = Z
        self.canvas.replot()

    def on_keyboard(self, event):
        print(event.accept())

    def setupCanvas(self):
        self.canvas = SlicerFigureCanvas()
        self.Container.addWidget(self.canvas)
        self.canvas.draw()

app = QtWidgets.QApplication(sys.argv)
window = mainwindow()
begradiger = Begradiger.Begradiger()

def showSpotauswertung():
    window.show()

def showBegradiger():
    begradiger.showMaximized()


if __name__ == '__main__':

    w = QtWidgets.QWidget()
    btn = QtWidgets.QPushButton("Auswertung Spots", w)
    btn2 = QtWidgets.QPushButton("Pkte Begradigen", w)
    btn.pressed.connect(showSpotauswertung)
    btn2.pressed.connect(showBegradiger)

    mainlayout = QtWidgets.QVBoxLayout()
    mainlayout.addWidget(btn)
    mainlayout.addWidget(btn2)
    w.setLayout(mainlayout)


    w.show()
    sys.exit(app.exec_())
