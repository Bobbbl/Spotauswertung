import sys
import PyQt5
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import FigureManagerQT
import numpy as np
import matplotlib.pyplot as plt

class Cutter(FigureCanvasQTAgg):

    auswahlGetroffen = QtCore.pyqtSignal()

    def __init__(self, Z, parent):
        self.fig = Figure()
        super().__init__(self.fig)
        self.ax = self.fig.add_subplot(111, aspect='equal')
        self.m_x = 10
        self.m_y = 10
        self.heightr = 10
        self.widthr = 10
        self.square = plt.Rectangle([self.m_x, self.m_y], self.widthr, self.heightr)
        self.ax.add_artist(self.square)

        self.Z = Z
        self.Z_cut = self.Z

        x = np.linspace(0, self.Z.shape[0], self.Z.shape[0])
        y = np.linspace(0, self.Z.shape[1], self.Z.shape[1])
        self.X, self.Y = np.meshgrid(x, y)
        self.ax.clear()
        self.line1 = self.ax.contourf(self.X, self.Y, self.Z, cmap=plt.cm.bone)
        self.ax.relim()
        self.draw()

        self.parentCanvas = parent




        self.mpl_connect('motion_notify_event', self.on_motion)
        self.mpl_connect('button_press_event', self.on_click)
        self.mpl_connect('scroll_event', self.on_spin)

    def on_motion(self, event):
        if not event.inaxes:
            return

        if event.xdata and event.ydata:
            xdata, ydata = event.xdata, event.ydata
            self.square.set_visible(False)
            self.m_x = xdata
            self.m_y = ydata
            self.square.set_x(self.m_x)
            self.square.set_y(self.m_y)
            self.draw()
            self.background = self.copy_from_bbox(self.ax.bbox)
            self.square.set_visible(True)
            self.restore_region(self.background)
            self.ax.draw_artist(self.square)
            self.blit(self.ax.bbox)

    def readSquare(self):
        Z = self.Z[int(self.m_x):int(self.m_x + self.square.get_width()), int(self.m_y):int(self.m_y + self.square.get_height())]
        return Z

    def on_click(self, event):
        if not event.inaxes:
            return
        if event.button == 1:
            self.parentCanvas.Z_cut = self.readSquare()
            self.auswahlGetroffen.emit()
            self.parentCanvas.replot()
            self.parentCanvas.draw()
            #self.parentCanvas.Z_cut = self.Z_cut


    def on_spin(self, event):
        if event.button is 'up' or event.button is 'down':
            self.square.set_visible(False)
            self.draw()
            self.background = self.copy_from_bbox(self.ax.bbox)
            self.square.set_visible(True)
            self.restore_region(self.background)
            self.widthr = self.widthr + event.step
            self.heightr = self.heightr + event.step
            self.square.set_width(self.widthr)
            self.square.set_height(self.heightr)
            self.ax.draw_artist(self.square)
            self.blit(self.ax.bbox)






if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    canvas = Cutter()
    canvas.show()
    sys.exit(app.exec_())