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

    name = 'Alternating Least Squares'
    tooltip = '''Runs alternating least squares regression analysis on a 2D
 data matrix and a 2D data matrix of components'''
    nDimension = 2
    nDataSets = 1
    version = 0.1


    def operation(self, DataOut, DataIn, Meta):
        """The generic 'main' function of an operation type user script."""
        # iterationNumber and convergenceSigma should, ideally, come from the
        # settings dialog/dictionary
        iterationNumber = 100
        convergenceSigma = 0.02

        dataInputObject = DataIn[0]
        componentInputObject = DataIn[1]
        dataInputArray = dataInputObject.matrix
        componentInputArray = componentInputObject.matrix
        if not (isinstance(dataInputArray, np.ndarray) and
                isinstance(componentInputArray, np.ndarray)):
            raise TypeError('Is not an array!')
        else:
            solution = vuvdeconvolution.als(dataInputArray,
                                            componentInputArray,
                                            numIter=iterationNumber,
                                            convSigma=convergenceSigma)
            outputObject = ScriptIOData()
            outputObject.matrix = solution
            DataOut.append(outputObject)
