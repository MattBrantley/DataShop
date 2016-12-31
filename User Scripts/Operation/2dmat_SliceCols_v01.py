# -*- coding: utf-8 -*-
"""
Takes a 2-dimensional matrix of size [m, n] and returns n vectors of length m.
"""

from UserScript import UserOperation, ScriptIOData
import numpy as np

class ds_user_script(UserOperation):
    """Creates a user script of the operation type."""

    name = 'Slice Columns'
    tooltip = 'Slices a 2D matrix and returns the columns'
    nDimension = 2
    nDataSets = 1

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
            for col in range(cols):
                Meta['Progress'] = round((col/cols)*100)
                dataOutputObject = ScriptIOData()
                dataOutputObject.matrix = dataInputArray[:, col]
                DataOut.append(dataOutputObject)
