 # -*- coding: utf-8 -*-
"""
Takes a 2-dimensional matrices of size [m, n] (data) and a i number of
1-dimensional matrices of size [1, m]. Returns the alternating least squares
solution matrices of sizes [i, n] and [i, m].
"""

from UserScript import *
import numpy as np
import vuvdeconvolution as vuv

class ds_user_script(UserOperation):
    """Creates a user script of the operation type."""

    name = 'Alternating Least Squares'
    tooltip = '''Runs alternating least squares regression analysis on a 2D
 data matrix and a 2D data matrix of components'''
    nDimension = 2
    nDataSets = 2
    version = 0.1

    vuvData = DataSetSettingsObject(minimum=1, maximum=1, primaryEnabled=True)
    vuvData.setDescription('A 2D VUV matrix')
    # The wave and time vectors should be replaced when the import scripts and
    # axes tracking are fully implemented.
    waveVector = DataSetSettingsObject(minimum=1, maximum=1)
    waveVector.setDescription('A 1D matrix with the wavelength numbers')
    timeVector = DataSetSettingsObject(minimum=1, maximum=1)
    timeVector.setDescription('A 1D matrix with the time points')
    components = DataSetSettingsObject(minimum=1, maximum=20)
    components.setDescription('''The components (either a series of individual
 components, or a single, stacked array of the components''')
    numIter = IntegerSettingsObject(minimum=1, maximum=10000000, default=100)
    numIter.setDescription('The number of iterations')
    conSigma = FloatSettingsObject(minimum=0.0, maximum=100.0, default=0.0)
    conSigma.setDescription('Stops the iterations when this sigma is achieved')

    settings = {'A. VUV Data': vuvData,
                'B. Wavelength Data': waveVector,
                'C. Time Data': timeVector,
                'D. Start Conditions': components,
                'E. Number of Iterations': numIter,
                'F. Convergence Sigma': conSigma
                }

    def operation(self, DataOut, Meta):
        """The generic 'main' function of an operation type user script."""
        # iterationNumber and convergenceSigma should, ideally, come from the
        # settings dialog/dictionary
        vuvData = Meta['A. VUV Data'][0].matrix
        waveVector = Meta['B. Wavelength Data'][0].matrix
        timeVector = Meta['C. Time Data'][0].matrix
        startConditions = Meta['D. Start Conditions']
        numIter = Meta['E. Number of Iterations']
        convSigma = Meta['F. Convergence Sigma']
        if len(startConditions) != 1:
            startCList = [startConditions[i].matrix for i, __ in
                          enumerate(startConditions)]
            startConditions = np.array(startCList)
        chromatograms, spectra = vuv.als(vuvData, startConditions,
                                         Meta, numIter=numIter,
                                         convSigma=convSigma)

        for i, spectrum in enumerate(spectra):
            outSpec = ScriptIOData()
            outSpec.matrix = spectrum
            outSpec.name = 'Spectrum {}'.format(i + 1)
            DataOut.append(outSpec)
        for i, chromatogram in enumerate(chromatograms):
            outChrom = ScriptIOData()
            outChrom.matrix = chromatogram
            outChrom.name = 'Chromatogram {}'.format(i + 1)
            DataOut.append(outChrom)
