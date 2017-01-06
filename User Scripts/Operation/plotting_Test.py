# -*- coding: utf-8 -*-
"""
Takes two 1-dimensional matrices of sizes m and n, multiplies each element to
form a 2-dimensional matrix of size [m,n].
"""

from UserScript import *
import numpy as np
import pyqtgraph.examples
from PyQt5 import QtGui
import pyqtgraph as pg


class ds_user_script(UserOperation):

    name = 'Plotting'
    tooltip = 'Plotting functions'
    nDimension = 1
    nDataSets = 2
    version = 0.5
    data = DataSetSettingsObject(minimum=1, maximum=1, primaryEnabled=True)
    data.setDescription('A 1D matrix')
    settings = {'A. Matrix': data}
    low = 0
    high = 0

    def operation(self, DataOut, Meta):
        data = Meta['A. Matrix'][0].matrix
        axis = Meta['A. Matrix'][0].axes[0]
        vector = axis.vector

        app = QtGui.QApplication([])
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        win = pg.GraphicsWindow(title="Basic plotting")
        win.resize(1000, 600)
        win.setWindowTitle('pyqtgraph example: Plotting')
        pg.setConfigOptions(antialias=True)
        ploty = win.addPlot(title="Region Selection")
        peny = pg.mkPen(color=(0, 0, 0), width=4)
        ploty.plot(vector, data, pen=peny)
        lr = pg.LinearRegionItem([np.amin(vector)*1.1, np.amax(vector)*0.9])
        lr.setZValue(-10)
        ploty.addItem(lr)

        def regionUpdated(regionItem):
            low, high = regionItem.getRegion()
            self.low = low
            self.high = high
        lr.sigRegionChanged.connect(regionUpdated)
        # pyqtgraph.examples.run()
        app.exec_()
        low = np.amax(np.where(vector<=self.low))
        high = np.amax(np.where(vector<=self.high))

        outData = ScriptIOData()
        outAxis = ScriptIOAxis()
        outAxis.name = axis.name
        outAxis.units = axis.units
        outAxis.vector = axis.vector[low:high]
        outData.matrix = data[low:high]
        outData.axes = [outAxis]
        DataOut.append(outData)