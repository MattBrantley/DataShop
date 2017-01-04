# -*- coding: utf-8 -*-
"""
Takes matrices of the same size and shape and multiplies the individual
elements.
"""

from UserScript import *
import numpy as np


class ds_user_script(UserOperation):
    """Creates a user script of the operation type."""

    name = 'Hadamard Matrix Multiplication'
    tooltip = 'Multiplies the entries of matrices of the same shape'
    nDimension = 2
    nDataSets = 100
    version = 0.3

    primaryMatrix = DataSetSettingsObject(primaryEnabled=True)
    primaryMatrix.setDescription('Primary matrix (retains axis information)')
    multiplicationMatrices = DataSetSettingsObject(minimum=1, maximum=100)
    multiplicationMatrices.setDescription('Matrices to be multiplied')
    settings = {'A. Primary Matrix': primaryMatrix,
                'B. Multiplication Matrices': multiplicationMatrices}

    def operation(self, DataOut, Meta):
        """The generic 'main' function of an operation type user script."""
        primaryMatrix = Meta['A. Primary Matrix'][0].matrix
        try:
            matrices = [matrix.matrix for matrix in
                        Meta['B. Multiplication Matrices']]
            shapes = [matrix.shape for matrix in matrices]
        except:
            print('Matrix Multiplication gone wrong!')
            pass
        if shapes.count(primaryMatrix.shape) == len(shapes):
            for matrix in matrices:
                primaryMatrix = primaryMatrix * matrix
        else:
            # Popup dialog
            raise ValueError('Matrices are not the same shape!')

        outputObject = ScriptIOData()
        outputObject.matrix = primaryMatrix
        DataOut.append(outputObject)
