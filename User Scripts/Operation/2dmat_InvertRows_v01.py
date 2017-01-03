# -*- coding: utf-8 -*-
"""
Takes a 2-dimensional matrix of size [m, n] and returns a matrix with the
row orders inverted.
"""

from UserScript import *
import numpy as np


class ds_user_script(UserOperation):
    """Creates a user script of the operation type."""

    name = 'Invert Rows'
    tooltip = 'Inverts the row order of a 2D matrix'
    nDimension = 2
    nDataSets = 1
    version = 0.1

    dataSet = DataSetSettingsObject(minimum=1, maximum=1, primaryEnabled=True)
    dataSet.setDescription('A 2D input matrix')

    settings = {'Input Matrix': dataSet}

    def operation(self, DataOut, Meta):
        """The generic 'main' function of an operation type user script."""

        dataInputMatrix = Meta['Input Matrix'][0].matrix
        # dataInputName = Meta['Input Matrix'][0].name

        if not isinstance(dataInputMatrix, np.ndarray):
            raise TypeError('Is not an array!')
        else:
            dataOutputObject = ScriptIOData()
            dataOutputObject.matrix = np.flipud(dataInputMatrix)
            # dataOutputObject.name = dataInputName
            DataOut.append(dataOutputObject)