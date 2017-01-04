# -*- coding: utf-8 -*-
"""
Takes a 2-dimensional matrix of size [m, n], an integer (i) of the number of
components for which to solve, and an offset value (defaults to 0.02).

The offset value may be optimized to yield better results.

Returns two matrices of sizes [m, i] and [n, i] of the suspected components
along the m and n axes, respectively.
"""

from UserScript import *
import numpy as np
import vuvdeconvolution

class ds_user_script(UserOperation):
    """Creates a user script of the operation type."""

    name = 'Simplisma'
    tooltip = 'Returns the results of the Simplisma algorithm on a matrix.'
    nDimension = 2
    nDataSets = 1
    version = 0.3

    vuvData = DataSetSettingsObject(minimum=1, maximum=1, primaryEnabled=True)
    vuvData.setDescription('A 2D VUV matrix')
    numComps = IntegerSettingsObject(minimum=2, maximum=25, default=2)
    numComps.setDescription('Number of components for which to solve')
    offset = IntegerSettingsObject(minimum=1, maximum=100, default=2)
    offset.setDescription('Simplisma offset value')

    settings = {'A. VUV Data': vuvData,
                'B. Number of Components': numComps,
                'C. Offset': offset,
                }

    def operation(self, DataOut, Meta):
        """The generic 'main' function of an operation type user script."""
        # self.DataIn is a list of ScriptIOData types. We want the first (or
        # slice [0]) of this list.
        vuvData = Meta['A. VUV Data'][0].matrix
        numComps = Meta['B. Number of Components']
        offset = Meta['C. Offset'] / 100

        results = vuvdeconvolution.simplisma(vuvData, numComps, offset)
        startChrom, startSpec, compSpec, puritySpec = results
        for i, spectrum in enumerate(startSpec):
            outputObject = ScriptIOData()
            outputObject.matrix = spectrum
            outputObject.name = 'Spectrum {}'.format(i+1)
            DataOut.append(outputObject)
        for i, chromatogram in enumerate(startChrom):
            outputObject = ScriptIOData()
            outputObject.matrix = chromatogram
            outputObject.name = 'Chromatogram {}'.format(i+1)
            DataOut.append(outputObject)

