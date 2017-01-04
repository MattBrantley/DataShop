# -*- coding: utf-8 -*-
"""
Takes matrices of the same size and shape and adds them.
"""

from UserScript import *
import numpy as np


class ds_user_script(UserOperation):
    """Creates a user script of the operation type."""

    name = 'Add Matrices'
    tooltip = 'Adds matrices of the same shape'
    nDimension = 2
    nDataSets = 100
    version = 0.3

    primaryMatrix = DataSetSettingsObject(primaryEnabled=True)
    primaryMatrix.setDescription('Primary matrix (retains axis information)')
    additionMatrices = DataSetSettingsObject(minimum=1, maximum=100)
    additionMatrices.setDescription('Matrices to be added')
    settings = {'A. Primary Matrix': primaryMatrix,
                'B. Addition Matrices': additionMatrices}

    def operation(self, DataOut, Meta):
        """The generic 'main' function of an operation type user script."""
        primaryMatrix = Meta['A. Primary Matrix'][0].matrix
        try:
            matrices = [matrix.matrix for matrix in
                        Meta['B. Addition Matrices']]
            shapes = [matrix.shape for matrix in matrices]
        except:
            print('Matrix Addition gone wrong!')
            pass
        if shapes.count(primaryMatrix.shape) == len(shapes):
            for matrix in matrices:
                primaryMatrix = np.add(primaryMatrix, matrix)
        else:
            # Popup dialog
            raise ValueError('Matrices are not the same shape!')

        outputObject = ScriptIOData()
        outputObject.matrix = primaryMatrix
        DataOut.append(outputObject)
