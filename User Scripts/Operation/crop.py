# -*- coding: utf-8 -*-

from UserScript import UserOperation, ScriptIOData
import numpy as np


class ds_user_script(UserOperation):
    """Creates a user script of the operation type."""

    name = 'Crop'
    tooltip = 'Crops a 1 or 2D data set.'
    nDimension = 2
    nDataSets = 1

    def operation(self):
        """The generic 'main' function of an operation type user script."""
        # self.DataIn is a list of ScriptIOData types. We want the first (or
        # slice [0]) of this list.
        dataInputObject = self.DataIn[0]
        # The first slice of this list contains a matrix attribute, that
        # should be a numpy array. If it is, we crop it.
        dataInputArray = dataInputObject.matrix
        if not isinstance(dataInputArray, np.ndarray):
            raise TypeError('Is not an array!')
        else:
            croppedArray = dataInputArray[1000:5000]
        # Create the output box for shipping, package the new data, and ship
        # it out.
        dataOutputObject = ScriptIOData()
        dataOutputObject.matrix = croppedArray
        self.DataOut.append(dataOutputObject)
