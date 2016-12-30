# -*- coding: utf-8 -*-

from UserScript import UserOperation, ScriptIOData
import numpy as np
import deconvolutionFunctions


class ds_user_script(UserOperation):
    """Creates a user script of the operation type."""

    name = 'Simplisma'
    tooltip = 'Returns the results of the Simplisma algorithm on a matrix.'
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
            numComps = 2
            offset = 0.02
            results = deconvolutionFunctions.simplisma(dataInputArray, numComps, offset)
            startChrom, startSpec, compSpec, puritySpec = results
        # Create the output box for shipping, package the new data, and ship
        # it out.
            chromatogramOutputObject = ScriptIOData()
            chromatogramOutputObject.matrix = startChrom
            self.DataOut.append(chromatogramOutputObject)
            spectrumOutputObject1 = ScriptIOData()
            spectrumOutputObject1.matrix = startSpec
            self.DataOut.append(spectrumOutputObject1)
            spectrumOutputObject2 = ScriptIOData()
            spectrumOutputObject2.matrix = compSpec
            self.DataOut.append(spectrumOutputObject2)
            spectrumOutputObject3 = ScriptIOData()
            spectrumOutputObject3.matrix = puritySpec
            self.DataOut.append(spectrumOutputObject3)