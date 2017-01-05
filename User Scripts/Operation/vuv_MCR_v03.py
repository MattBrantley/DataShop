# -*- coding: utf-8 -*-
"""
Takes a 2-dimensional matrix of size [m, n], an integer (i) of the number of
components for which to solve, and a noise value (defaults to 0.01).

The noise value may be optimized to yield better results.

Returns a matrices of size [m, i] of the suspected components
along the m axis.
"""

from UserScript import *
import numpy as np
#import vuvdeconvolution as vuv

class ds_user_script(UserOperation):
    """Creates a user script of the operation type."""

    name = 'Multivariate Curve Resolution'
    tooltip = 'Runs the MCR algorithm on a 2D matrix'
    nDimension = 2
    nDataSets = 1
    version = 0.1

    vuvData = DataSetSettingsObject(minimum=1, maximum=1, primaryEnabled=True)
    vuvData.setDescription('A 2D VUV matrix')
    numComps = IntegerSettingsObject(minimum=2, maximum=25, default=2)
    numComps.setDescription('Number of components for which to solve')
    noise = IntegerSettingsObject(minimum=1, maximum=100, default=1)
    noise.setDescription('MCR noise value')

    settings = {'A. VUV Data': vuvData,
                'B. Number of Components': numComps,
                'C. Noise': noise,
                }
    def operation(self, DataOut, Meta):
        """The generic 'main' function of an operation type user script."""

        vuvData = Meta['A. VUV Data'][0].matrix
        numComps = Meta['B. Number of Components']
        noise = Meta['C. Noise'] / 100

        results = vuv.mcr(vuvData, numComps, noise).T
        for i, result in enumerate(results):
            outputObject = ScriptIOData()
            outputObject.matrix = result
            outputObject.name = 'Result {}'.format(i + 1)
            DataOut.append(outputObject)