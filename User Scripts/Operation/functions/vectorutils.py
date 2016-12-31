# coding=utf-8
"""
Utility functions for working with vector data.
"""

import scipy.interpolate
import numpy as np


def r2calc(yMeas, yRef):
    """Calculates the R-squared value for two vectors"""
    # =========================================================================
    # If the number of y points in the measured and reference vectors are not
    # equivalent, iterpolates the measured vector to have the same number of
    # data points as the reference spectra.
    # =========================================================================
    if len(yMeas) != len(yRef):
        interpolate = scipy.interpolate.interp1d
        yMeas = interpolate(np.arange(len(yMeas)), yMeas, kind='linear',
                            fill_value='extrapolate')(np.arange(len(yRef)))
    # =========================================================================
    # Produces a correlation coefficient matrix of the y values.
    # =========================================================================
    rMatrix = np.corrcoef(yMeas, yRef)
    r2 = rMatrix[0][1] ** 2
    return r2
