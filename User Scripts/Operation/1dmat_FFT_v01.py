# -*- coding: utf-8 -*-
"""
Returns the fast Fourier Transform of a 1-D matrix.
"""

from UserScript import *
import numpy as np


class ds_user_script(UserOperation):
    """Creates a user script of the operation type."""

    name = 'Fast Fourier Transform'
    tooltip = 'Computes the fast Fourier Transform of a matrix'
    nDimension = 1
    nDataSets = 1
    version = 0.3

    primaryMatrix = DataSetSettingsObject(primaryEnabled=True)
    primaryMatrix.setDescription('Primary matrix (retains axis information)')
    settings = {'Matrix': primaryMatrix}

    def operation(self, DataOut, Meta):
        """The generic 'main' function of an operation type user script."""
        matrix = Meta['Matrix'][0].matrix
        try:
            matrixFFT = np.fft.fft(matrix)
            outputReal = ScriptIOData()
            outputReal.matrix = matrixFFT.real
            outputReal.name = 'Real'
            outputImaginary = ScriptIOData()
            outputImaginary.matrix = matrixFFT.imag
            outputImaginary.name = 'Imaginary'
            DataOut.append(outputReal)
            DataOut.append(outputImaginary)
        except:
            print('Matrix subtraction gone wrong!')
            pass
