# -*- coding: utf-8 -*-
"""
Takes a 2-dimensional matrix and normalizes it against the greatest value
point. Defaults to normalizing matrix to 1.
"""

from UserScript import UserOperation, ScriptIOData
import numpy as np

class ds_user_script(UserOperation):
    """Creates a user script of the operation type."""

    name = 'Normalize'
    tooltip = 'Normalizes a 2D matrix'
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
            maximum = np.max(dataInputArray)
            dataOutputObject = ScriptIOData()
            dataOutputObject.matrix = dataInputArray / maximum
            DataOut.append(dataOutputObject)