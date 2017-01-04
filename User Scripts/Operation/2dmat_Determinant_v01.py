# -*- coding: utf-8 -*-
"""
Takes a 2-dimensional, square matrix [m, m] and returns the determinant.
"""

from UserScript import *
import numpy as np


class ds_user_script(UserOperation):
    """Creates a user script of the operation type."""

    name = 'Determinant'
    tooltip = 'Computes the determinant of a square matrix'
    nDimension = 2
    nDataSets = 1
    version = 0.3

    DataSet = DataSetSettingsObject(minimum=1, maximum=1, primaryEnabled=True)
    DataSet.setDescription('An input Matrix of size [m, n]')

    settings = {'Input Matrix': DataSet}

    def operation(self, DataOut, Meta):
        """The generic 'main' function of an operation type user script."""
        # self.DataIn is a list of ScriptIOData types. We want the first (or
        # slice [0]) of this list.
        dataInputMatrix = Meta['Input Matrix'][0].matrix
        dataInputName = Meta['Input Matrix'][0].name

        if not isinstance(dataInputMatrix, np.ndarray):
            raise TypeError('Is not an array!')
        else:
            try:
                determinate = np.linalg.det(dataInputMatrix)
                dOut = ScriptIOData()
                dOut.matrix = determinate
                dOut.name = '{}'.format(determinate)
                DataOut.append(dOut)
            except:
                # Should have popup message about error
                pass

