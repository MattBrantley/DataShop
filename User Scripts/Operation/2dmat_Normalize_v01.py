# -*- coding: utf-8 -*-
"""
Takes a 2-dimensional matrix and normalizes it against the greatest value
point. Defaults to normalizing matrix to 1.
"""

from UserScript import *
import numpy as np


class ds_user_script(UserOperation):
    """Creates a user script of the operation type."""

    name = 'Normalize'
    tooltip = 'Normalizes a 2D matrix'
    nDimension = 2
    nDataSets = 1
    version = 0.3

    dataSet = DataSetSettingsObject(minimum=1, maximum=1, primaryEnabled=True)
    dataSet.setDescription('A 2D input matrix')

    settings = {'Input Matrix': dataSet}

    def operation(self, DataOut, Meta):
        """The generic 'main' function of an operation type user script."""

        dataInputMatrix = Meta['Input Matrix'][0].matrix
        # dataInputName = Meta['Input Matrix'][0].name

        if not isinstance(dataInputMatrix, np.ndarray):
            raise TypeError('Is not an array!')
        else:
            maximum = np.max(dataInputMatrix)
            dataOutputObject = ScriptIOData()
            dataOutputObject.matrix = dataInputMatrix / maximum
            dataOutputObject.name = 'Normalized Matrix'
            DataOut.append(dataOutputObject)
