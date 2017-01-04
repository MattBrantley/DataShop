# -*- coding: utf-8 -*-
"""
Takes a 2-dimensional matrix of size [m, n] and returns a summed vector of
length n.
"""

from UserScript import *
import numpy as np

class ds_user_script(UserOperation):
    """Creates a user script of the operation type."""

    name = 'Sum Columns'
    tooltip = 'Sums the columns of a 2D matrix'
    nDimension = 2
    nDataSets = 1
    version = 0.3

    DataSet = DataSetSettingsObject(minimum=1, maximum=1, primaryEnabled=True)
    DataSet.setDescription('An input matrix')

    settings = {'Input Matrix': DataSet}

    def operation(self, DataOut, Meta):
        """The generic 'main' function of an operation type user script."""
        dataInputMatrix = Meta['Input Matrix'][0].matrix
        row, col = dataInputMatrix.shape
        # The first slice of this list contains a matrix attribute, that
        # should be a numpy array.
        if not isinstance(dataInputMatrix, np.ndarray):
            raise TypeError('Is not an array!')
        else:
            dataOutputObject = ScriptIOData()
            dataOutputObject.matrix = np.sum(dataInputMatrix, axis=1)
            dataOutputObject.name = 'Result x{}'.format(row)
            DataOut.append(dataOutputObject)