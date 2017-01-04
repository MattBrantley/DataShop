# -*- coding: utf-8 -*-
"""
Takes two 2-dimensional matrices of size [m, n] (data) and [i, m] (i amount of
starting components of 1D arrays m). Returns the classical least squares
solution matrix of size [i, n].
"""

from UserScript import *
import numpy as np
import vuvdeconvolution as vuv

class ds_user_script(UserOperation):
    """Creates a user script of the operation type."""
    # TODO: Add background subtraction
    name = 'Classical Least Squares'
    tooltip = '''Runs the CLS algorithm on a 2D data matrix and a 2D component
 matrix'''
    nDimension = 2
    nDataSets = 1
    version = 0.3

    primaryMatrix = DataSetSettingsObject(primaryEnabled=True)
    primaryMatrix.setDescription('Primary matrix (retains axis information)')
    componentMatrices = DataSetSettingsObject(minimum=1, maximum=25)
    componentMatrices.setDescription('Component matrices')
    settings = {'A. Data Matrix': primaryMatrix,
                'B. Component Matrices': componentMatrices}

    def operation(self, DataOut, Meta):
        """The generic 'main' function of an operation type user script."""
        primaryMatrix = Meta['A. Data Matrix'][0].matrix
        componentMatrices = Meta['B. Component Matrices']
        if len(componentMatrices) != 1:
            cList = [componentMatrices[i].matrix for i, __ in
                     enumerate(componentMatrices)]
            componentMatrices = np.array(cList)
        results = vuv.cls(primaryMatrix, componentMatrices)
        for i, result in enumerate(results):
            outSpec = ScriptIOData()
            outSpec.matrix = result
            outSpec.name = 'Result {}'.format(i + 1)
            DataOut.append(outSpec)

