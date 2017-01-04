# -*- coding: utf-8 -*-
"""
Takes a 2-dimensional matrix of size [m, n] and returns the standard deviation
of the nubmers within the matrix.
"""

from UserScript import *
import numpy as np

class ds_user_script(UserOperation):
    """Creates a user script of the operation type."""

    name = 'Standard Deviation'
    tooltip = 'Computes the standard deviation of a matrix'
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
            standardDeviation = np.std(dataInputMatrix)
            dataOutputObject = ScriptIOData()
            dataOutputObject.matrix = standardDeviation
            dataOutputObject.name = '{}'.format(round(standardDeviation, 4))
            DataOut.append(dataOutputObject)