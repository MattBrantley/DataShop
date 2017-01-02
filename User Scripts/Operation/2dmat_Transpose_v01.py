# -*- coding: utf-8 -*-
"""
Takes a 2-dimensional matrix of size [m, n] and returns a transposed matrix of
size [n, m].
"""

# from UserScript import UserOperation, ScriptIOData
# from UserScriptSettingsObjects import DataSetSettingsObject as DSSO
from UserScript import *
import numpy as np

class ds_user_script(UserOperation):
    """Creates a user script of the operation type."""
    # Meta-data and information for the GUI
    name = 'Transpose'
    tooltip = 'Transposes a 2D matrix'
    nDimension = 2
    nDataSets = 1
    version = 0.1

    # Defines the input data parameter (the right clicked object here)
    DataSet = DataSetSettingsObject(minimum=1, maximum=1, primaryEnabled=True)
    DataSet.setDescription('An input Matrix of size [m, n]')

    # Defines the settings toolbox that will pop up if there is more than 1
    # setting.
    settings = {'Input Matrix': DataSet}

    def operation(self, DataOut, Meta):
        """The generic 'main' function of an operation type user script."""

        dataInputObject = Meta['Input Matrix']
        # The first slice of this list contains a matrix attribute, that
        # should be a numpy array.
        if not isinstance(dataInputObject, np.ndarray):
            raise TypeError('Is not an array!')
        else:
            transposedArray = np.transpose(dataInputObject)
            outputObject = ScriptIOData()
            outputObject.matrix = transposedArray
            DataOut.append(outputObject)
