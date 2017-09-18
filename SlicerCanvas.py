import sys
import PyQt5
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import FigureManagerQT
import numpy as np
import time
import matplotlib.pyplot as plt
from PyQt5 import QtCore
import Exceptions
from mpl_toolkits.mplot3d import Axes3D
from Filter import savitzky_golay
from scipy.signal import argrelextrema
from matplotlib.animation import FuncAnimation



class Update(object):
    def __init__(self, line, x):
        self.x = x
        self.phase = 0
        self.line = line
    def __call__(self, _):
        self.line.set_ydata(np.cos(self.x + self.phase / 5.0))
        self.phase += 1.0
        return [self.line]


class SlicerFigureCanvas(FigureCanvasQTAgg):


    def __init__(self, Z=None):
        self.fig = Figure()
        super(SlicerFigureCanvas, self).__init__(self.fig)
        self.background = None
        self.backgroundc = None
        self.backgroundr = None
        self.draggable = None

        self.Z = Z
        self.disco = False
        self.row = None
        self.col = None
        self.r = 10
        self.m = (0,0)
        self.startr = 0
        self.stopr = 0
        self.startc = 0
        self.stopc = 0
        self.filterWidth2 = 3
        self.filterWidth3 = 3
        self.filterOrder2 = 1
        self.filterOrder3 = 1
        self.motionEvent = None
        self.scrollEvent = None
        self.maximar = None
        self.minimar = None
        self.maximac = None
        self.minimac = None
        self.markersr = None
        self.markersc = None
        self.draggabler = None
        self.draggablec = None
        self.Z_cut = self.Z

        self.line4 = None

        self.ax1 = self.figure.add_subplot(222, aspect='equal')
        self.ax2 = self.figure.add_subplot(223)
        self.ax3 = self.figure.add_subplot(224)
        self.ax4 = self.figure.add_subplot(221, aspect='equal')

        self.lx = self.ax1.axhline(color='k')  # the horiz line
        self.ly = self.ax1.axvline(color='k')  # the vert line
        self.circle = plt.Circle(self.m, self.r, color='r', alpha=0.3)
        self.rx = 0
        self.ry = 0
        self.rwidth = 20
        self.rheight = 20
        self.square = plt.Rectangle([self.rx,self.ry], self.rwidth, self.rheight)
        self.ax1.add_artist(self.circle)
        self.ax1.add_artist(self.lx)
        self.ax1.add_artist(self.ly)
        self.ax4.add_artist(self.square)

        if self.Z is not None:
            self.replot()
        else:
            self.cancelPlot()

        #Connect
        self.mpl_connect('button_press_event', self.on_click)
        self.mpl_connect('motion_notify_event', self.on_move_cut)
        self.mpl_connect('button_release_event', self.on_release)
        #self.mpl_disconnect(self.motionEvent)
        #self.mpl_disconnect(self.scrollEvent)


    def on_move_cut(self, event):
        if not event.inaxes:
            return
        xdata = event.xdata
        ydata = event.ydata
        self.square.set_visible(False)
        self.square.set_x(xdata)
        self.square.set_y(ydata)
        self.draw()
        self.background_cut = self.copy_from_bbox(self.ax4.bbox)
        self.square.set_visible(True)
        self.restore_region(self.background_cut)
        self.update()


    def on_release(self, event):
        self.draggabler = None
        self.draggablec = None

    def on_click(self, event):
        if event.button == 1:
            x = event.x
            y = event.y
            xydatar = self.ax2.transData.transform(self.markersr.get_xydata())
            xdatar,ydatar = xydatar.T
            xy = self.ax2.transData.transform((x,y))
            xydatac = self.ax3.transData.transform(self.markersc.get_xydata())
            xdatac, ydatac = xydatac.T
            rr = ((xdatar - x) ** 2 + (ydatar - y) ** 2) ** 0.5
            rc = ((xdatac - x) ** 2 + (ydatac - y) ** 2) ** 0.5
            print(np.min(rr))

            if np.min(rr) < 20:
                self.markersr.set_visible(False)
                self.draw()
                self.backgroundr = self.copy_from_bbox(self.ax2.bbox)
                self.markersr.set_visible(True)
                self.ax2.draw_artist(self.markersr)
                self.update()
                self.draw()
                self.draggabler = np.argmin(rr)
            else:
                self.draggabler = None

            if np.min(rc) < 20:
                self.markersc.set_visible(False)
                self.draw()
                self.backgroundc = self.copy_from_bbox(self.ax3.bbox)
                self.markersc.set_visible(True)
                self.ax3.draw_artist(self.markersc)
                self.update()
                self.draggablec = np.argmin(rc)
                #self.draggable = np.argmin(self.markersc)

            else:
                self.draggablec = None

        if event.button == 3:
            x = event.x
            y = event.y
            xydatar = self.ax2.transData.transform(self.markersr.get_xydata())
            xdatar, ydatar = xydatar.T
            xydatac = self.ax3.transData.transform(self.markersc.get_xydata())
            xdatac, ydatac = xydatac.T
            rr = ((xdatar - x) ** 2 + (ydatar - y) ** 2) ** 0.5
            rc = ((xdatac - x) ** 2 + (ydatac - y) ** 2) ** 0.5

            if np.min(rr) < 20:
                self.markersr.set_visible(False)
                self.draw()
                self.backgroundr = self.copy_from_bbox(self.ax2.bbox)
                self.markersr.set_visible(True)
                self.ax2.draw_artist(self.markersr)
                self.draggabler = np.argmin(rr)
                xdata,ydata = self.markersr.get_data()
                if self.markersr is not None:
                    self.markersr.remove()
                self.maximar = np.delete(self.maximar, self.draggabler)
                self.draggabler = None
                self.plotRowNoExtrema(self.rowplot)
                self.restore_region(self.backgroundr)
                self.ax2.draw_artist(self.markersr)
                self.update()
                self.draw()
            if np.min(rc) < 20:
                self.markersc.set_visible(False)
                self.draw()
                self.backgroundc = self.copy_from_bbox(self.ax3.bbox)
                self.markersc.set_visible(True)
                self.ax2.draw_artist(self.markersc)
                self.draggablec = np.argmin(rc)
                xdata,ydata = self.markersr.get_data()
                if self.markersc is not None:
                    self.markersc.remove()
                self.maximac = np.delete(self.maximac, self.draggablec)
                self.draggablec = None
                self.plotColNoExtrema(self.colplot)
                self.restore_region(self.backgroundc)
                self.ax3.draw_artist(self.markersc)
                self.update()
                self.draw()





    # Slot
    def setFilterWidth2(self, width):
        if type(width) is not int:
            return
        if width % 2 != 1 or width < 1:
            return
        self.filterWidth2 = width
        self.readRowCircle()
        self.rowplot = savitzky_golay(self.rowplot, self.filterWidth2, self.filterOrder2)
        self.plotRow(self.rowplot)
        self.update()
        self.draw()
        print(self.filterWidth2)

    def setFilterOrder2(self, order):
        if type(order) is not int:
            return
        if self.filterWidth2 % 2 != 1 or self.filterWidth2 < 1:
            return
        self.filterOrder2 = order
        self.readRowCircle()
        self.rowplot = savitzky_golay(self.rowplot, self.filterWidth2, self.filterOrder2)
        self.plotRow(self.rowplot)
        self.update()
        self.draw()

    def setFilterWidth3(self, width):
        if type(width) is not int:
            return
        if width % 2 != 1 or width < 1:
            return
        self.filterWidth3 = width
        self.readColCircle()
        self.colplot = savitzky_golay(self.colplot, self.filterWidth3, self.filterOrder3)
        self.plotCol(self.colplot)
        self.update()
        self.draw()

    def setFilterOrder3(self, order):
        if type(order) is not int:
            return
        if self.filterWidth3 % 2 != 1 or self.filterWidth3 < 1:
            return
        self.filterOrder3 = order
        self.readColCircle()
        self.colplot = savitzky_golay(self.colplot, self.filterWidth3, self.filterOrder3)
        self.plotCol(self.colplot)
        self.update()
        self.draw()

    def refreshSanchezArtists(self):
        self.ax1.draw_artist(self.lx)
        self.ax1.draw_artist(self.ly)
        self.ax1.draw_artist(self.circle)


    def replot(self):
        x = np.linspace(0, self.Z_cut.shape[0], self.Z_cut.shape[0])
        y = np.linspace(0, self.Z_cut.shape[1], self.Z_cut.shape[1])
        self.X, self.Y = np.meshgrid(x, y)
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.line4 = self.ax4.contourf(self.X, self.Y, self.Z_cut, cmap=plt.cm.bone)
        self.line2 = self.ax2.plot(np.linspace(0, self.Z_cut.max(), self.Z_cut.shape[0]))
        self.line3 = self.ax3.plot(np.linspace(0, self.Z_cut.max(), self.Z_cut.shape[0]))
        self.ax4.relim()
        self.draw()

        self.motionEvent = self.mpl_connect('motion_notify_event', self.on_motion)
        self.scrollEvent = self.mpl_connect('scroll_event', self.on_spin)
        self.disco = False

    def cancelPlot(self):
        #self.mpl_disconnect(self.motionEvent)
        #self.mpl_disconnect(self.scrollEvent)
        self.disco = True

    def reconnectPlot(self):
        self.motionEvent = self.mpl_connect('motion_notify_event', self.on_motion)
        self.scrollEvent = self.mpl_connect('scroll_event', self.on_spin)
        self.disco = False

    def getData(self):
        tmp = self.Z_cut[self.startr:self.stopr, self.startc:self.stopc]
        return tmp

    def on_spin(self, event):
        if event.button is 'up' or event.button is 'down':
            self.r = self.r + event.step
            self.circle.set_radius(self.r)
            self.lx.set_visible(False)
            self.ly.set_visible(False)
            self.circle.set_visible(False)
            self.draw()
            self.background = self.copy_from_bbox(self.ax1.bbox)
            self.lx.set_visible(True)
            self.ly.set_visible(True)
            self.circle.set_visible(True)
            self.restore_region(self.background)
            self.readRowCircle()
            self.readColCircle()
            self.rowplot = savitzky_golay(self.rowplot, self.filterWidth2, self.filterOrder2)
            self.colplot = savitzky_golay(self.colplot, self.filterWidth3, self.filterOrder3)
            self.plotRow(self.rowplot)
            self.plotCol(self.colplot)
            self.update()
            self.refreshSanchezArtists()


    def on_motion(self, event):
        if not event.inaxes:
            return

        if self.draggabler is not None:
            if event.xdata and event.ydata:
                xdatar, ydatar = self.markersr.get_data()
                xindexr = np.argmin(np.abs(self.line2[0].get_xdata() - event.xdata))
                ydatar[self.draggabler] = self.line2[0].get_ydata()[xindexr]
                xdatar[self.draggabler] = self.line2[0].get_xdata()[xindexr]
                self.maximar[self.draggabler] = self.line2[0].get_xdata()[xindexr]
                self.markersr.set_xdata(xdatar)
                self.markersr.set_ydata(ydatar)
                self.restore_region(self.backgroundr)
                self.ax2.draw_artist(self.markersr)
                self.update()
        elif self.draggablec is not None:
            if event.xdata and event.ydata:
                xdatac, ydatac = self.markersc.get_data()
                xindexc = np.argmin(np.abs(self.line3[0].get_xdata() - event.xdata))
                ydatac[self.draggablec] = self.line3[0].get_ydata()[xindexc]
                xdatac[self.draggablec] = self.line3[0].get_xdata()[xindexc]
                self.maximac[self.draggablec] = self.line2[0].get_xdata()[xindexc]
                self.markersc.set_xdata(xdatac)
                self.markersc.set_ydata(ydatac)
                self.restore_region(self.backgroundc)
                self.ax3.draw_artist(self.markersc)
                self.update()

        if self.disco:
            return
        if self.draggabler is None and self.draggablec is None:
            xdata = event.xdata
            ydata = event.ydata
            self.lx.set_visible(False)
            self.ly.set_visible(False)
            self.circle.set_visible(False)
            self.lx.set_ydata(ydata)
            self.ly.set_xdata(xdata)
            self.m = (xdata,ydata)
            self.circle.center = self.m
            self.draw()
            self.background = self.copy_from_bbox(self.ax1.bbox)
            self.lx.set_visible(True)
            self.ly.set_visible(True)
            self.circle.set_visible(True)
            self.restore_region(self.background)
            self.row = int(np.floor(ydata))
            self.col = int(np.floor(xdata))
            self.readRowCircle()
            self.readColCircle()
            self.rowplot = savitzky_golay(self.rowplot,self.filterWidth2, self.filterOrder2)
            self.colplot = savitzky_golay(self.colplot, self.filterWidth3, self.filterOrder3)
            self.plotRow(self.rowplot)
            self.plotCol(self.colplot)
            self.update()
            self.draw()
            self.ax1.draw_artist(self.lx)
            self.ax1.draw_artist(self.ly)
            self.ax1.draw_artist(self.circle)
            #self.blit(self.ax1.bbox)
            #self.blit(self.ax2.bbox)
            #self.blit(self.ax3.bbox)
            #self.blit(self.ax4.bbox)





    def readRowCircle(self):
        startr = int(np.floor(self.m[0] - self.r))
        if startr < 0:
            startr = 0
        stopr = int(np.floor(self.m[0] + self.r))
        if stopr > self.Z_cut.shape[1]:
            stopr = self.Z_cut.shape[1]
        self.rowplot = self.Z_cut[int(np.floor(self.m[1])), startr:stopr]
        self.startr = startr
        self.stopr = stopr

    def readColCircle(self):
        startc = int(np.floor(self.m[1] - self.r))
        if startc < 0:
            startc = 0
        stopc = int(np.floor(self.m[1] + self.r))
        if stopc > self.Z_cut.shape[0]:
            stopc = self.Z_cut.shape[0]
        self.colplot = self.Z_cut[int(np.floor(self.m[0])), startc:stopc]
        self.startc = startc
        self.stopc = stopc

    def plotRowNoExtrema(self, y):
        x = np.linspace(0, len(y), len(y))
        self.ax2.relim()
        self.ax2.autoscale_view(True, True, True)
        self.markersr, = self.ax2.plot(x[self.maximar], y[self.maximar], marker='o', markeredgecolor = 'r', color='r', ms=6, linestyle='None')
        self.line2[0].set_xdata(x)
        self.line2[0].set_ydata(y)

    def plotColNoExtrema(self,y):
        x = np.linspace(0, len(y), len(y))
        self.ax3.relim()
        self.ax3.autoscale_view(True, True, True)
        self.markersc, = self.ax3.plot(x[self.maximac], y[self.maximac], marker='o',markeredgecolor = 'r', color='r', ms=6, linestyle='None')
        self.line3[0].set_xdata(x)
        self.line3[0].set_ydata(y)

    def plotRow(self, y):
        x = np.linspace(0, len(y), len(y))
        self.ax2.relim()
        self.ax2.autoscale_view(True, True, True)
        self.maximar = argrelextrema(y, np.greater, order=20)
        self.minimar = argrelextrema(y, np.less, order=20)
        self.maximar = np.hstack([0, self.maximar[0], self.minimar[0], len(y)-1])
        self.maximar = np.sort(self.maximar)
        if self.markersr is not None:
            self.markersr.remove()
        self.markersr, = self.ax2.plot(x[self.maximar], y[self.maximar], marker='o', markeredgecolor = 'r', color='r', ms=6, linestyle='None')
        self.line2[0].set_xdata(x)
        self.line2[0].set_ydata(y)

    def plotCol(self, y):
        x = np.linspace(0, len(y), len(y))
        self.ax3.relim()
        self.ax3.autoscale_view(True, True, True)
        self.maximac = argrelextrema(y, np.greater, order=20)
        self.minimac = argrelextrema(y, np.less, order=20)
        self.maximac = np.hstack([0, self.maximac[0], self.minimac[0], len(y)-1])
        self.maximac = np.sort(self.maximac)
        if self.markersc is not None:
            self.markersc.remove()
        self.markersc, = self.ax3.plot(x[self.maximac], y[self.maximac], marker='o', markeredgecolor = 'r', color='r', ms=6, linestyle='None')
        self.line3[0].set_xdata(x)
        self.line3[0].set_ydata(y)


def plotSlice(Z):
    app = QtWidgets.QApplication(sys.argv)
    canvas = SlicerFigureCanvas()
    manager = FigureManagerQT(canvas, 1)
    manager.show()
    app.exec_()
    sys.exit(0)  # Temp
