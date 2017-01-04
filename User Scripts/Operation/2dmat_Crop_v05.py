# -*- coding: utf-8 -*-
"""
Takes a 2-dimensional matrix of size [m, n] and returns a cropped Matrix.
"""

from UserScript import *
import numpy as np

class ds_user_script(UserOperation):
    """Creates a user script of the operation type."""
    # Meta-data and information for the GUI
    name = 'Crop Matrix'
    tooltip = 'Crop Matrix'
    nDimension = 2
    nDataSets = 1
    version = 0.5

    # Defines the input data parameter (the right clicked object here)
    DataSet = DataSetSettingsObject(minimum=1, maximum=1, primaryEnabled=True)
    DataSet.setDescription('An input Matrix')
    axisToCrop = IntegerSettingsObject(minimum=0, maximum=10, default=0)
    axisBeginCrop = FloatSettingsObject()
    axisEndCrop = FloatSettingsObject()


    # Defines the settings toolbox that will pop up if there is more than 1
    # setting.
    settings = {'Input Matrix': DataSet,
                'Axis to Crop': axisToCrop,
                'Begin Crop': axisBeginCrop,
                'End Crop': axisEndCrop}

    def operation(self, DataOut, Meta):
        """The generic 'main' function of an operation type user script."""

        dataInputObject = Meta['Input Matrix'][0].matrix
        beginCrop = Meta['Begin Crop']
        endCrop = Meta['End Crop']
        axisNumber = Meta['Axis to Crop']

        dataAxisObject = Meta['Input Matrix'][0].axes
        dataAxisList = dataAxisObject[axisNumber].vector
        beginIndex = len(np.where(dataAxisList <= beginCrop)[0])
        endIndex = len(np.where(dataAxisList <= endCrop)[0]) + 1
        indices = np.arange(beginIndex, endIndex)
        newDataAxis = np.array(dataAxisList[beginIndex:endIndex])
        newMatrix = np.take(dataInputObject, indices, axisNumber)

        outputObject = ScriptIOData()
        outputObject.matrix = newMatrix
        for i, axis in enumerate(dataAxisObject):
            if i == axisNumber:
                newAxis = ScriptIOAxis()
                newAxis.name = axis.name
                newAxis.units = axis.units
                newAxis.vector = newDataAxis
                outputObject.axes.append(newAxis)
            else:
                outputObject.axes.append(axis)
        DataOut.append(outputObject)
