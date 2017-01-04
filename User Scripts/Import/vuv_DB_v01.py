# -*- coding: utf-8 -*-
'''
Connects to the provided VUV file (a .db, database file) via sqlite,
extracts the data, crops it, and returns three numpy arrays of the time
points, the wavelength points, and the data matrix that corresponds to the
time points and wavelength points.
'''

from UserScript import *
import vuvdeconvolution as vuv

class ds_user_script(UserImport):
    """Creates a user script of the import type."""

    name = 'VUV .db Importer'
    registeredFiletypes = {'VUV .db files': '.db'}
    tooltip = 'Imports a VUV .db file'
    nDimension = 2
    nDataSets = 1
    version = 0.3

    def import_func(self, DataOut, URL, FileName):
        try:
            timePts, λPts, vuvArray = vuv.extractvuv(URL)
            timeAxis = ScriptIOAxis()
            timeAxis.vector = timePts
            timeAxis.units = 'minutes'
            timeAxis.name = 'Time'
            waveAxis = ScriptIOAxis()
            waveAxis.vector = λPts
            waveAxis.units = 'nano meters'
            waveAxis.name = 'Wavelength'
            outputData = ScriptIOData()
            outputData.matrix = vuvArray
            outputData.name = FileName
            outputData.axes.append(waveAxis)
            outputData.axes.append(timeAxis)
            DataOut.append(outputData)
            return True
        except ValueError:
            print('Import Error, .db might be corrupted.')
            return False
