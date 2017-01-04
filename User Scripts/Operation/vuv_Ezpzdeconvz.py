# -*- coding: utf-8 -*-
"""
Takes a 2-dimensional matrix of size [m, n] and deconvolutes it.
"""

from UserScript import *
import numpy as np
import vuvdeconvolution as vuv


class ds_user_script(UserOperation):
    """Creates a user script of the operation type."""

    name = 'Ezpzdeconvz'
    tooltip = 'Deconvolutes a VUV matrix'
    nDimension = 2
    nDataSets = 1
    version = 0.5

    vuvData = DataSetSettingsObject(minimum=1, maximum=1, primaryEnabled=True)
    vuvData.setDescription('A 2D VUV matrix')
    numComp = IntegerSettingsObject(minimum=1, maximum=20, default=2)
    numComp.setDescription('Number of convoluted components')
    # startTime = FloatSettingsObject(minimum=0.0, default=0.0)
    # startTime.setDescription('Start Time (min)')
    # endTime = FloatSettingsObject(minimum=0.0, default=60)
    # endTime.setDescription('End Time (min)')
    # startWave = FloatSettingsObject(minimum=0.0, default=125)
    # startWave.setDescription('Start Wavelength (nm)')
    # endWave = FloatSettingsObject(minimum=0.0, default=240)
    # endWave.setDescription('End Wavelength (nm)')

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

    userLibrary = FileSelectionSettingsObject(filter='*.json')
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
                'B. Number of Components': numComp,
                # 'C. Start Time (min)': startTime,
                # 'D. End Time (min)': endTime,
                # 'E. Start Wave (nm)': startWave,
                # 'F. End Wave (nm)': endWave,
                'C. Start Conditions': startConditions,
                'D. Simplisma Offset %': simpOffset,
                'E. MCR Noise': mcrNoise,
                'F. User Spectra': userSpectra,
                'G. User Library': userLibrary,
                'H. Deconvolution Method': deconMethod,
                'I. Number of Iterations': numIter,
                'J. Convergence Sigma': convSigma
                }

    def operation(self, DataOut, Meta):
        """The generic 'main' function of an operation type user script."""

        vuvData = Meta['A. VUV Data'][0].matrix
        a1 = Meta['A. VUV Data'][0].axes[0]
        a2 = Meta['A. VUV Data'][0].axes[1]
        numComp = Meta['B. Number of Components']
        # startTime = Meta['C. Start Time (min)']
        # endTime = Meta['D. End Time (min)']
        # startWave = Meta['E. Start Wave (nm)']
        # endWave = Meta['F. End Wave (nm)']
        startConditions = Meta['C. Start Conditions']
        simpOffset = Meta['D. Simplisma Offset %'] / 100
        mcrNoise = Meta['E. MCR Noise'] / 100
        userSpectra = Meta['F. User Spectra']
        userLibrary = Meta['G. User Library']
        deconMethod = Meta['H. Deconvolution Method']
        numIter = Meta['I. Number of Iterations']
        convSigma = Meta['J. Convergence Sigma']

        vuvRow, vuvCol = vuvData.shape
        if (vuvRow == len(a1.vector)) and (vuvCol == len(a2.vector)):
            pass
        elif (vuvCol == len(a1.vector)) and (vuvRow == len(a2.vector)):
            a1, a2 = a2, a1
            print('Transposed!!')
        else:
            raise ValueError('Vectors do not align with the data!')

        axis1 = a1.vector
        axis2 = a2.vector
        # startWaveIndex = len(np.where(axis1 <= startWave)[0])
        # endWaveIndex = len(np.where(axis1 <= endWave)[0]) + 1
        # startTimeIndex = len(np.where(axis2 <= startTime)[0])
        # endTimeIndex = len(np.where(axis2 <= endTime)[0]) + 1
        # vuvData = vuvData[startWaveIndex:endWaveIndex, startTimeIndex:endTimeIndex]
        print(vuvData.shape)
        # waveVector = np.array(axis1[startWaveIndex:endWaveIndex])
        waveVector= axis1
        waveName = a1.name
        waveUnits = a1.units
        # timeVector = np.array(axis2[startTimeIndex:endTimeIndex])
        timeVector = axis2
        timeName = a2.name
        timeUnits = a2.units

        if type(userLibrary) == str:
            library = vuv.getlibrary(userLibrary)
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
                raise ValueError('No library found')
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
                raise ValueError('No library found')
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
                outInitAx = ScriptIOAxis()
                outInitAx.name = waveName
                outInitAx.units = waveUnits
                outInitAx.vector = waveVector
                outInit.matrix = yVal
                outInit.name = 'Mat {}: {}'.format(i+1, result)
                outInit.axes.append(outInitAx)
                DataOut.append(outInit)
                outR2 = ScriptIOData()
                outR2Ax = ScriptIOAxis()
                outR2Ax.name = 'R squared'
                outR2Ax.units = 'None'
                outR2Ax.vector = np.array([1])
                outR2.axes.append(outR2Ax)
                outR2.matrix = np.array([r2])
                outR2.name = 'R2 {}: {}'.format(i+1, round(r2, 4))
                DataOut.append(outR2)
        if library:
            for i, spectrum in enumerate(spectra):
                result, r2, data = vuv.searchspectra(waveVector, spectrum,
                                                     library, returnList=False)
                yVal = vuv.interpolatespectra(data[0], data[1], waveVector)
                outLib = ScriptIOData()
                outLibAx = ScriptIOAxis()
                outLibAx.name = waveName
                outLibAx.units = waveUnits
                outLibAx.vector = waveVector
                outLib.axes.append(outLibAx)
                outLib.matrix = np.array(yVal)
                outLib.name = 'Match {}: {}'.format(i+1, result)
                DataOut.append(outLib)
                outR2 = ScriptIOData()
                outR2Ax = ScriptIOAxis()
                outR2Ax.name = 'R squared'
                outR2Ax.units = 'None'
                outR2Ax.vector = np.array([1])
                outR2.axes.append(outR2Ax)
                outR2.matrix = np.array([r2])
                outR2.name = 'R2 {}: {}'.format(i+1, round(r2, 4))
                DataOut.append(outR2)

        for i, spectrum in enumerate(spectra):
            outSpec = ScriptIOData()
            outSpecAx = ScriptIOAxis()
            outSpecAx.name = waveName
            outSpecAx.units = waveUnits
            outSpecAx.vector = waveVector
            outSpec.axes.append(outSpecAx)
            outSpec.matrix = spectrum
            outSpec.name = 'Spectrum {}'.format(i + 1)
            DataOut.append(outSpec)
        for i, chromatogram in enumerate(chromatograms):
            outChrom = ScriptIOData()
            outChromAx = ScriptIOAxis()
            outChromAx.name = timeName
            outChromAx.units = timeUnits
            outChromAx.vector = timeVector
            outChrom.axes.append(outChromAx)
            outChrom.matrix = chromatogram
            outChrom.name = 'Chromatogram {}'.format(i + 1)
            DataOut.append(outChrom)

