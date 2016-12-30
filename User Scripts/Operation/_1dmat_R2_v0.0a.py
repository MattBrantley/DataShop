# -*- coding: utf-8 -*-
"""
Takes two 1-dimensional matrices, compares them, and returns the R2 value.
"""

from UserScript import UserOperation, ScriptIOData
import numpy as np
import vectorutils


class ds_user_script(UserOperation):
    """Creates a user script of the operation type."""

    name = 'R2 Comparison'
    tooltip = 'Computes the R2 value of two 1D matrices'
    nDimension = 1
    nDataSets = 2
    version = 0.1

    def operation(self):
        """The generic 'main' function of an operation type user script."""
        vectorInputObject1 = self.DataIn[0]
        vectorInputObject2 = self.DataIn[1]
        vector1 = vectorInputObject1.matrix
        vector2 = vectorInputObject2.matrix
        if not (isinstance(vector1, np.ndarray) and
                isinstance(vector2, np.ndarray)):
            raise TypeError('Is not an array!')
        else:
            r2 = vectorutils.r2calc(vector1, vector2)
            outputObject = ScriptIOData()
            outputObject.matrix = r2
            self.DataOut.append(outputObject)
