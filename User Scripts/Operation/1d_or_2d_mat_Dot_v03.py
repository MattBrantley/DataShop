# -*- coding: utf-8 -*-
"""
Takes matrices of sizes [m,n] and [n,m] and returns the dot product.
"""

from UserScript import *
import numpy as np


class ds_user_script(UserOperation):
    """Creates a user script of the operation type."""

    name = 'Dot Product'
    tooltip = 'Returns the dot product of two matrices'
    nDimension = 2
    nDataSets = 2
    version = 0.3

    primaryMatrix = DataSetSettingsObject(primaryEnabled=True)
    primaryMatrix.setDescription('Primary matrix (retains axis information)')
    dotMatrix = DataSetSettingsObject(minimum=1, maximum=1)
    dotMatrix.setDescription('Dot product matrix')
    settings = {'A. Primary Matrix [m,n]': primaryMatrix,
                'B. Matrix [n,m]': dotMatrix}

    def operation(self, DataOut, Meta):
        """The generic 'main' function of an operation type user script."""
        primaryMatrix = Meta['A. Primary Matrix [m,n]'][0].matrix
        dotMatrix = Meta['B. Matrix [n,m]'][0].matrix
        try:
            outMatrix = primaryMatrix @ dotMatrix
            outputObject = ScriptIOData()
            outputObject.matrix = outMatrix
            DataOut.append(outputObject)
        except:
            print('Dot Product gone wrong!')
            pass


