# -*- coding: utf-8 -*-
"""
Takes a 2-dimensional matrix of size [m, n], an integer (i) of the number of
components for which to solve, and a noise value (defaults to 0.01).

The noise value may be optimized to yield better results.

Returns a matrices of size [m, i] of the suspected components
along the m axis.
"""

from UserScript import UserOperation, ScriptIOData
import numpy as np
import vuvdeconvolution

class ds_user_script(UserOperation):
    """Creates a user script of the operation type."""

    name = 'Multivariate Curve Resolution'
    tooltip = 'Runs the MCR algorithm on a 2D matrix'
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
            numComps = 2
            noise = 0.01
            results = vuvdeconvolution.mcr(dataInputArray, numComps, noise)
            startSpec = results
            # Create the output box for shipping, package the new data, and
            # ship it out.
            spectraOutputObject = ScriptIOData()
            spectraOutputObject.matrix = startSpec
            self.DataOut.append(spectraOutputObject)