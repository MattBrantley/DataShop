# -*- coding: utf-8 -*-
"""
Takes a 2-dimensional matrix of size [m, n], an integer (i) of the number of
components for which to solve, and an offset value (defaults to 0.02).

The offset value may be optimized to yield better results.

Returns two matrices of sizes [m, i] and [n, i] of the suspected components
along the m and n axes, respectively.
"""

from UserScript import UserOperation, ScriptIOData
import numpy as np
import vuvdeconvolution

class ds_user_script(UserOperation):
    """Creates a user script of the operation type."""

    name = 'Simplisma'
    tooltip = 'Returns the results of the Simplisma algorithm on a matrix.'
    nDimension = 2
    nDataSets = 1
    version = 0.1

    def operation(self, DataOut, DataIn, Meta):
        """The generic 'main' function of an operation type user script."""
        # self.DataIn is a list of ScriptIOData types. We want the first (or
        # slice [0]) of this list.
        dataInputObject = DataIn[0]
        # The first slice of this list contains a matrix attribute, that
        # should be a numpy array.
        dataInputArray = dataInputObject.matrix
        if not isinstance(dataInputArray, np.ndarray):
            raise TypeError('Is not an array!')
        else:
            numComps = 2
            offset = 0.02
            results = vuvdeconvolution.simplisma(dataInputArray,
                                                 numComps, offset)
            startChrom, startSpec, compSpec, puritySpec = results
            # Create the output box for shipping, package the new data, and
            # ship it out.
            chromatogramOutputObject = ScriptIOData()
            chromatogramOutputObject.matrix = startChrom
            DataOut.append(chromatogramOutputObject)
            spectrumOutputObject1 = ScriptIOData()
            spectrumOutputObject1.matrix = startSpec
            DataOut.append(spectrumOutputObject1)
            spectrumOutputObject2 = ScriptIOData()
            spectrumOutputObject2.matrix = compSpec
            DataOut.append(spectrumOutputObject2)
            spectrumOutputObject3 = ScriptIOData()
            spectrumOutputObject3.matrix = puritySpec
            DataOut.append(spectrumOutputObject3)
