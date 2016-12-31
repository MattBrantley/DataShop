# -*- coding: utf-8 -*-
"""
Takes two 2-dimensional matrices of size [m, n] (data) and [i, m] (i amount of
starting components of 1D arrays m). Returns the classical least squares
solution matrix of size [i, n].
"""

from UserScript import UserOperation, ScriptIOData
import numpy as np
import vuvdeconvolution

class ds_user_script(UserOperation):
    """Creates a user script of the operation type."""

    name = 'Classical Least Squares'
    tooltip = '''Runs the CLS algorithm on a 2D data matrix and a 2D component
 matrix'''
    nDimension = 2
    nDataSets = 1
    version = 0.1

    def operation(self):
        """The generic 'main' function of an operation type user script."""
        dataInputObject = self.DataIn[0]
        componentInputObject = self.DataIn[1]
        dataInputArray = dataInputObject.matrix
        componentInputArray = componentInputObject.matrix
        if not (isinstance(dataInputArray, np.ndarray) and
                isisntance(componentInputArray, np.ndarray)):
            raise TypeError('Is not an array!')
        else:
            solution = vuvdeconvolution.cls(dataInputArray,
                                            componentInputArray)
            outputObject = ScriptIOData()
            outputObject.matrix = solution
            self.DataOut.append(outputObject)

