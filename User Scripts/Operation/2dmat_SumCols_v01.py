# -*- coding: utf-8 -*-
"""
Takes a 2-dimensional matrix of size [m, n] and returns a summed vector of
length n.
"""

from UserScript import UserOperation, ScriptIOData
import numpy as np

class ds_user_script(UserOperation):
    """Creates a user script of the operation type."""

    name = 'Sum Columns'
    tooltip = 'Sums the columns of a 2D matrix'
    nDimension = 2
    nDataSets = 1
    version = 0.1

    def operation(self, DataOut, DataIn, Meta):
        """The generic 'main' function of an operation type user script."""
        # self.DataIn is a list of ScriptIOData types. We want the first (or
        # slice [0]) of this list.
        dataInputObject = DataIn[0]
        # The first slice of this list contains a matrix attribute, that
        # should be a numpy array.
        dataInputArray = dataInputObject.matrix
        if not isinstance(dataInputArray, np.ndarray):
            raise TypeError('Is not an array!')
        else:
            rows, cols = dataInputArray.shape
            dataOutputObject = ScriptIOData()
            dataOutputObject.matrix = np.sum(dataInputArray, axis=1)
            DataOut.append(dataOutputObject)