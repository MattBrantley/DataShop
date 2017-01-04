# -*- coding: utf-8 -*-
"""
Takes a 2-dimensional matrix of size [m, n] and returns a summed vector of
length m.
"""

from UserScript import *
import numpy as np

class ds_user_script(UserOperation):
    """Creates a user script of the operation type."""

    name = 'Sum Axis'
    tooltip = 'Sums the axis of a 2D matrix'
    nDimension = 2
    nDataSets = 1
    version = 0.3

    dataSet = DataSetSettingsObject(minimum=1, maximum=1, primaryEnabled=True)
    sumAxis = IntegerSettingsObject(minimum=0, default=0)
    dataSet.setDescription('An input matrix')
    sumAxis.setDescription('The axis number to sum')

    settings = {'Matrix': dataSet,
                'Axis': sumAxis}

    def operation(self, DataOut, Meta):
        """The generic 'main' function of an operation type user script."""
        dataSet = Meta['Matrix'][0].matrix
        sumAxis = Meta['Axis']
        dataOut = ScriptIOData()
        axisOut = ScriptIOAxis()
        for i, axis in enumerate(Meta[Matrix][0].axes):
            if i != sumAxis:
                axisOut.append(axis)
        dataOut.matrix = np.sum(dataInputMatrix, axis=sumAxis)
        DataOut.append(dataOut)