# -*- coding: utf-8 -*-
"""
Takes a 2-dimensional matrix of size [m, n] and returns a transposed matrix of
size [n, m].
"""

from UserScript import *
import numpy as np

class ds_user_script(UserOperation):
    """Creates a user script of the operation type."""
    # Meta-data and information for the GUI
    name = 'Transpose'
    tooltip = 'Transposes a 2D matrix'
    nDimension = 2
    nDataSets = 1
    version = 0.5

    # Defines the input data parameter (the right clicked object here)
    DataSet = DataSetSettingsObject(minimum=1, maximum=1, primaryEnabled=True)
    DataSet.setDescription('An input Matrix of size [m, n]')

    # Defines the settings toolbox that will pop up if there is more than 1
    # setting.
    settings = {'Input Matrix': DataSet}

    def operation(self, DataOut, Meta):
        """The generic 'main' function of an operation type user script."""

        dataInputObject = Meta['Input Matrix'][0].matrix
        dataNameObject = Meta['Input Matrix'][0].name
        dataAxisObject1 = Meta['Input Matrix'][0].axes[0]
        dataAxisObject2 = Meta['Input Matrix'][0].axes[1]

        if not isinstance(dataInputObject, np.ndarray):
            raise TypeError('Is not an array!')
        else:
            transposedArray = np.transpose(dataInputObject)
            outputObject = ScriptIOData()
            outputObject.matrix = transposedArray
            outputObject.axes = [dataAxisObject2, dataAxisObject1]
            outputObject.name = 'Transposed_{}'.format(dataNameObject)
            DataOut.append(outputObject)
