# -*- coding: utf-8 -*-
"""
Takes a 2-dimensional, square matrix [m, m] and returns the determinant.
"""

from UserScript import UserOperation, ScriptIOData
import numpy as np

class ds_user_script(UserOperation):
    """Creates a user script of the operation type."""

    name = 'Determinant'
    tooltip = 'Computes the determinant of a square matrix'
    nDimension = 2
    nDataSets = 1
    version = 0.1

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
            dataOutputObject = ScriptIOData()
            dataOutputObject.matrix = np.linalg.det(dataInputArray)
            self.DataOut.append(dataOutputObject)