# -*- coding: utf-8 -*-
"""
Takes matrices of the same size and shape and subtracts them.
"""

from UserScript import *
import numpy as np


class ds_user_script(UserOperation):
    """Creates a user script of the operation type."""

    name = 'Subtract Matrices'
    tooltip = 'Subtracts matrices of the same shape'
    nDimension = 2
    nDataSets = 100
    version = 0.3

    primaryMatrix = DataSetSettingsObject(primaryEnabled=True)
    primaryMatrix.setDescription('Primary matrix (retains axis information)')
    additionMatrices = DataSetSettingsObject(minimum=1, maximum=100)
    additionMatrices.setDescription('Matrices to be subtracted')
    settings = {'A. Primary Matrix': primaryMatrix,
                'B. Subtraction Matrices': additionMatrices}

    def operation(self, DataOut, Meta):
        """The generic 'main' function of an operation type user script."""
        primaryMatrix = Meta['A. Primary Matrix'][0].matrix
        try:
            matrices = [matrix.matrix for matrix in
                        Meta['B. Subtraction Matrices']]
            shapes = [matrix.shape for matrix in matrices]
        except:
            print('Matrix subtraction gone wrong!')
            pass
        if shapes.count(primaryMatrix.shape) == len(shapes):
            for matrix in matrices:
                primaryMatrix = np.subtract(primaryMatrix, matrix)
        else:
            # Popup dialog
            raise ValueError('Matrices are not the same shape!')

        outputObject = ScriptIOData()
        outputObject.matrix = primaryMatrix
        DataOut.append(outputObject)
