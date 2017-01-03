# -*- coding: utf-8 -*-
"""
Takes a 2-dimensional matrix of size [m, n] and returns m vectors of length n.
"""

from UserScript import *
import numpy as np

class ds_user_script(UserOperation):
    """Creates a user script of the operation type."""

    name = 'Slice Rows'
    tooltip = 'Slices a 2D matrix and returns the rows'
    nDimension = 2
    nDataSets = 1
    version = 0.3

    dataSet = DataSetSettingsObject(minimum=1, maximum=1, primaryEnabled=True)
    dataSet.setDescription('A 2D input matrix')

    settings = {'Input Matrix': dataSet}

    def operation(self, DataOut, Meta):
        """The generic 'main' function of an operation type user script."""

        dataInputMatrix = Meta['Input Matrix'][0].matrix

        if not isinstance(dataInputMatrix, np.ndarray):
            raise TypeError('Is not an array!')
        else:
            rows, cols = dataInputMatrix.shape
            for row in range(rows):
                Meta['Progress'] = round((row/rows)*100)
                dataOutputObject = ScriptIOData()
                dataOutputObject.matrix = dataInputMatrix[row]
                dataOutputObject.name = 'Row {}'.format(row+1)
                DataOut.append(dataOutputObject)

