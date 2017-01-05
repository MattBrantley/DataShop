# -*- coding: utf-8 -*-
"""
Takes two 1-dimensional matrices, compares them, and returns the R2 value.
"""

from UserScript import *
import numpy as np
#import vectorutils


class ds_user_script(UserOperation):
    """Creates a user script of the operation type."""

    name = 'R2 Comparison'
    tooltip = 'Computes the R2 value of two 1D matrices'
    nDimension = 1
    nDataSets = 2
    version = 0.3

    Vector1 = DataSetSettingsObject(minimum=1, maximum=1, primaryEnabled=True)
    Vector1.setDescription('The first 1D matrix')
    Vector2 = DataSetSettingsObject(minimum=1, maximum=1)
    Vector2.setDescription('The second 1D matrix')

    settings = {'1D Matrix 1': Vector1,
                '1D Matrix 2': Vector2}

    def operation(self, DataOut, Meta):
        """The generic 'main' function of an operation type user script."""
        vector1Object = Meta['1D Matrix 1'][0].matrix
        vector2Object = Meta['1D Matrix 2'][0].matrix
        if not (isinstance(vector1Object, np.ndarray) and
                isinstance(vector2Object, np.ndarray)):
            raise TypeError('Is not an array!')
        else:
            r2 = vectorutils.r2calc(vector1Object, vector2Object)
            outputObject = ScriptIOData()
            outputObject.matrix = r2
            outputObject.name = '{}'.format(r2)
            DataOut.append(outputObject)
