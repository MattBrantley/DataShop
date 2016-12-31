# -*- coding: utf-8 -*-
"""
Takes a 2-dimensional matrix of size [m, n] and returns m vectors of length n.
"""

from UserScript import UserOperation, ScriptIOData
import numpy as np

class ds_user_script(UserOperation):
    """Creates a user script of the operation type."""

    name = 'Slice Rows'
    tooltip = 'Slices a 2D matrix and returns the rows'
    nDimension = 2
    nDataSets = 1

    def operation(self):
        """The generic 'main' function of an operation type user script."""
        # self.DataIn is a list of ScriptIOData types. We want the first (or
        # slice [0]) of this list.
        dataInputObject = self.DataIn[0]
        # The first slice of this list contains a matrix attribute, that
        # should be a numpy array.
        dataInputArray = dataInputObject.matrix
        if not isinstance(dataInputArray, np.ndarray):
            raise TypeError('Is not an array!')
        else:
            rows, cols = dataInputArray.shape
            for row in range(rows):
                dataOutputObject = ScriptIOData()
                dataOutputObject.matrix = dataInputArray[row]
                self.DataOut.append(dataOutputObject)
