# -*- coding: utf-8 -*-
"""
Takes a 2-dimensional matrix of size [m, n] and deconvolutes it.
"""

from UserScript import *
import numpy as np
import vuvdeconvolution as vuv
import tkinter
import tkinter.filedialog


class ds_user_script(UserOperation):
    """Creates a user script of the operation type."""

    name = 'Ezpzdeconvz'
    tooltip = 'Deconvolutes a VUV matrix'
    nDimension = 2
    nDataSets = 1
    version = 0.1

    vuvData = DataSetSettingsObject(minimum=1, maximum=1, primaryEnabled=True)
    vuvData.setDescription('A 2D VUV matrix')
    # The wave and time vectors should be replaced when the import scripts and
    # axes tracking are fully implemented.
    waveVector = DataSetSettingsObject(minimum=1, maximum=1)
    waveVector.setDescription('A 1D matrix with the wavelength numbers')
    timeVector = DataSetSettingsObject(minimum=1, maximum=1)
    timeVector.setDescription('A 1D matrix with the time points')

    numComp = IntegerSettingsObject(minimum=1, maximum=20, default=2)
    numComp.setDescription('Number of convoluted components')
    startTime = FloatSettingsObject(minimum=0.0, default=0.0)
    startTime.setDescription('Start Time (min)')
    endTime = FloatSettingsObject(minimum=0.0, default=60)
    endTime.setDescription('End Time (min)')
    startWave = FloatSettingsObject(minimum=0.0, default=125)
    startWave.setDescription('Start Wavelength (nm)')
    endWave = FloatSettingsObject(minimum=0.0, default=240)
    endWave.setDescription('End Wavelength (nm)')

    startConditions = RingSettingsObject()
    startConditions.setDescription('Starting conditions')
    simplisma = startConditions.addSelection('Simplisma')
    altSimplisma = startConditions.addSelection('Alternative Simplisma')
    mcr = startConditions.addSelection('MCR')
    spectra = startConditions.addSelection('User Provided Spectra')
    simpLib = startConditions.addSelection('Simplisma -> Library Search')
    simpAlsLib = startConditions.addSelection('Simplisma -> ALS -> Library Search')
    startConditions.setDefault(simplisma)

    simpOffset = IntegerSettingsObject(minimum=0, maximum=100, default=2)
    simpOffset.setDescription('% Offset value for Simplisma')
    mcrNoise = FloatSettingsObject(minimum=0, maximum=100, default=1)
    userSpectra = DataSetSettingsObject(minimum=0, maximum=20, default=0)
    userSpectra.setDescription('User Provided Spectra (if selected)')

    userLibrary = BoolSettingsObject(default=False)
    userLibrary.setDescription('User is providing a library')

    deconMethod = RingSettingsObject()
    deconMethod.setDescription('Deconvolution Method')
    deconMethod.addSelection('Alternating Least Squares (ALS)')
    deconMethod.addSelection('Classic Least Squares (CLS)')

    numIter = IntegerSettingsObject(minimum=1, maximum=10000000, default=100)
    numIter.setDescription('Number of ALS iterations')
    convSigma = FloatSettingsObject(minimum=0.0, maximum=100, default=0.00)
    convSigma.setDescription('ALS convergence sigma')

    libCheckResults = BoolSettingsObject(default=False)
    libCheckResults.setDescription('Library match the deconvolution results')

    settings = {'A. VUV Data': vuvData,
                'B. Wavelength Data': waveVector,
                'C. Time Data': timeVector,
                'D. Number of Components': numComp,
                'E. Start Time (min)': startTime,
                'F. End Time (min)': endTime,
                'G. Start Wave (nm)': startWave,
                'H. End Wave (nm)': endWave,
                'I. Start Conditions': startConditions,
                'J. Simplisma Offset %': simpOffset,
                'K. MCR Noise': mcrNoise,
                'L. User Spectra': userSpectra,
                'M. User Library': userLibrary,
                'N. Deconvolution Method': deconMethod,
                'O. Number of Iterations': numIter,
                'P. Convergence Sigma': convSigma
                }

    def operation(self, DataOut, Meta):
        """The generic 'main' function of an operation type user script."""

        vuvData = Meta['A. VUV Data'][0].matrix
        waveVector = Meta['B. Wavelength Data'][0].matrix
        timeVector = Meta['C. Time Data'][0].matrix
        numComp = Meta['D. Number of Components']
        startTime = Meta['E. Start Time (min)']
        endTime = Meta['F. End Time (min)']
        startWave = Meta['G. Start Wave (nm)']
        endWave = Meta['H. End Wave (nm)']
        startConditions = Meta['I. Start Conditions']
        simpOffset = Meta['J. Simplisma Offset %'] / 100
        mcrNoise = Meta['K. MCR Noise'] / 100
        userSpectra = Meta['L. User Spectra']
        userLibrary = Meta['M. User Library']
        deconMethod = Meta['N. Deconvolution Method']
        numIter = Meta['O. Number of Iterations']
        convSigma = Meta['P. Convergence Sigma']

        vuvRow, vuvCol = vuvData.shape
        if (len(waveVector.shape) != 1) or (len(timeVector.shape) != 1):
            raise ValueError('vectors too many dimensions (expected 1-D)')
        if (vuvRow == len(waveVector)) and (vuvCol == len(timeVector)):
            pass
        elif (vuvCol == len(waveVector)) and (vuvrow == len(timeVector)):
            vuvData = vuvData.T
        else:
            raise ValueError('Vectors do not align with the data!')

        startWaveIndex = np.argmin(waveVector <= startWave) - 1
        endWaveIndex = np.argmax(waveVector >= endWave) + 1
        startTimeIndex = np.argmin(timeVector <= startTime) - 1
        endTimeIndex = np.argmin(timeVector <= endTime) + 1
        waveVector = np.array(waveVector[startWaveIndex:endWaveIndex])
        timeVector = np.array(timeVector[startTimeIndex:endTimeIndex])

        if userLibrary:
            library = vuv.getlibrary()
        else:
            library = None
        initialMatches = []

        if startConditions == 'Simplisma':
            results = vuv.simplisma(vuvData, numComp, simpOffset)
            sChrom, sSpec, cSpec, pSpec = results
            startingSpectra = sSpec
        elif startConditions == 'Alternative Simplisma':
            results = vuv.simplisma(vuvData, numComp, simpOffset)
            sChrom, sSpec, cSpec, pSpec = results
            startingSpectra = cSpec
        elif startConditions == 'MCR':
            startingSpectra = vuv.mcr(vuvData, numComp, mcrNoise)
        elif startConditions == 'User Provided Spectra':
            sList = [userSpectra[i].matrix for i, _ in enumerate(userSpectra)]
            startingSpectra = np.array(sList)
        elif startConditions == 'Simplisma -> Library Search':
            if not library:
                library = vuv.getlibrary()
            results = vuv.simplisma(vuvData, numComp, simpOffset)
            sChrom, sSpec, cSpec, pSpec = results
            intermediateSpectra = sSpec
            # This is repeated below, possibly push into function?
            startingSpectra = []
            for spectrum in intermediateSpectra:
                results = vuv.searchspectra(waveVector, spectrum,
                                            library, returnList=False)
                initialMatches.append(results)
                name, r2, data = results
                addSpec = vuv.interpolatespectra(data[0], data[1], waveVector)
                startingSpectra.append(addSpec)
            startingSpectra = np.array(startingSpectra)
        elif startConditions == 'Simplisma -> ALS -> Library Search':
            if not library:
                library = vuv.getlibrary()
            results = vuv.simplisma(vuvData, numComp, simpOffset)
            sChrom, sSpec, cSpec, pSpec = results
            intermediateSpectra = vuv.als(vuvData, sSpec,
                                          Meta, numIter=numIter,
                                          convSigma=convSigma)[1]
            # Here's where it begins to repeat.
            startingSpectra = []
            for spectrum in intermediateSpectra:
                results = vuv.searchspectra(waveVector, spectrum,
                                            library, returnList=False)
                initialMatches.append(results)
                name, r2, data = results
                addSpec = vuv.interpolatespectra(data[0], data[1], waveVector)
                startingSpectra.append(addSpec)
            startingSpectra = np.array(startingSpectra)
        else:
            raise ValueError('Start conditions unresolvable!')
        if deconMethod == 'Alternating Least Squares (ALS)':
            chromatograms, spectra = vuv.als(vuvData, startingSpectra,
                                             Meta, numIter=numIter,
                                             convSigma=convSigma)
        elif deconMethod == 'Classic Least Squares (CLS)':
            chromatograms = vuv.cls(vuvData, startingSpectra)
            spectra = startingSpectra
        else:
            raise ValueError('Unexpected Deconvolution Method')

        if initialMatches:
            for i, spectrum in enumerate(initialMatches):
                result, r2, data = spectrum
                yVal = vuv.interpolatespectra(data[0], data[1], waveVector)
                outInit = ScriptIOData()
                outInit.matrix = yVal
                outInit.name = 'Mat {}: {}'.format(i+1, result)
                DataOut.append(outInit)
                outR2 = ScriptIOData()
                outR2.matrix = r2
                outR2.name = 'R2 {}: {}'.format(i+1, round(r2, 4))
                DataOut.append(outR2)
        if library:
            for i, spectrum in enumerate(spectra):
                result, r2, data = vuv.searchspectra(waveVector, spectrum,
                                                     library, returnList=False)
                yVal = vuv.interpolatespectra(data[0], data[1], waveVector)
                outLib = ScriptIOData()
                outLib.matrix = np.array(yVal)
                outLib.name = 'Match {}: {}'.format(i+1, result)
                DataOut.append(outLib)
                outR2 = ScriptIOData()
                outR2.matrix = r2
                outR2.name = 'R2 {}: {}'.format(i+1, round(r2, 4))
                DataOut.append(outR2)

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

