# coding=utf-8
"""
Deconvolution functions for working with Vacuum Ultraviolet Data.
"""
import numpy as np
import json
from scipy import optimize
import scipy.interpolate
from PyQt5.QtWidgets import QFileDialog
import tkinter
import tkinter.filedialog
import sqlite3
import struct

def simplisma(vuvMat, nComps, offset):
    """
    Takes the truncated data set, the offset (indicating the amount of allowed
    divergence -- smaller is better for higher quality data), and the number
    of suspected components and returns starting chromatograms.
    """
    # =========================================================================
    # Calculates constants -- np.divide and / are used somewhat interchangeably
    # =========================================================================
    nλPts, numTimePts = vuvMat.shape
    σ = np.std(vuvMat, axis=0, ddof=1) * np.sqrt(nλPts-1)/np.sqrt(nλPts)
    μ = np.mean(vuvMat, axis=0)
    α = offset * np.max(μ)
    λ = np.sqrt((σ*σ + (α+μ)*(α+μ))*np.sqrt(nλPts))
    scaledMat = np.matrix(np.divide(vuvMat, λ))
    purity = np.divide(σ, (α+μ))
    # =========================================================================
    # Finds purity indexes and uses them to find some component spectra
    # (compSpec) in the VUV data set.
    # =========================================================================
    pureIndex = []
    pureλ = np.zeros((vuvMat.shape[0], 0))
    for __ in range(nComps+1):
        weight = []
        for num in range(numTimePts):
            pureλeval = np.append(pureλ, scaledMat[:, num], axis=1)
            covariance = pureλeval.conj().T * pureλeval
            weight.append(np.linalg.det(covariance))
        puritySpec = weight * purity
        maxIndex = np.where(puritySpec == np.max(puritySpec))[0][0]
        pureIndex.append(maxIndex)
        pureλ = scaledMat[:,pureIndex]
    puritySpec = pureλ
    compSpec = vuvMat[:,pureIndex[:nComps]]
    # =========================================================================
    # Solves least squares matrices to provide starting spectra and starting
    # chromatograms. The component spectra and purity spectra (should be the
    # same as one another, but with differing scaling amounts) are also
    # returned, as they may be useful as alternate starting spectra.
    # =========================================================================
    corrSpec = np.linalg.lstsq(compSpec, vuvMat)[0]
    correlation = np.linalg.lstsq(corrSpec.T, vuvMat.T)[0]
    totalSignal = np.sum(vuvMat.conj().T, axis=0).conj()
    scaleFact = np.diag(np.linalg.lstsq(correlation.T, totalSignal)[0])
    startSpec = np.dot(correlation.T, scaleFact).T
    startChrom = np.dot(np.linalg.inv(scaleFact), corrSpec)
    return startChrom, startSpec, compSpec, puritySpec


def mcr(vuvMat, numComps, noise):
    '''Althernate method of purity spectra generation.'''
    # Calculates a large number of constants and a few dot products
    nRow, nCol = vuvMat.shape
    σ = np.std(vuvMat, axis=0, ddof=1)
    μ = np.mean(vuvMat, axis=0)
    scaledNoise = max(μ)*noise + μ
    l = np.sqrt(σ*σ + (scaledNoise)*(scaledNoise))
    p = np.divide(σ, (scaledNoise))
    pureIndex = [np.argmax(p)]
    dl = np.array([vuvMat[:,i] / l[i] for i in range(nCol)]).T
    c = np.dot(dl.conj().T, dl) / nRow
    w = σ*σ + μ*μ / (l*l)
    p = p * w
    ww = np.zeros((numComps, nCol))
    ww[0] = w
    pp = np.zeros((numComps, nCol))
    pp[0] = p
    maxPure = [p[pureIndex][0]]
    # Quadruple for loop - not pretty; untested if running a three-component
    # mixture!
    for i in range(1, numComps):
        for j in range(nCol):
            dm = np.zeros((i+1, i+1))
            dm[0][0] = c[j][j]
            for k in range(i):
                kvar = pureIndex[k]
                dm[0][k+1] = c[j][kvar]
                dm[k+1][0] = c[kvar][j]
                for l in range(i):
                    lvar = pureIndex[l]
                    dm[k+1][l+1] = c[kvar][lvar]
            ww[i][j] = np.linalg.det(dm)
            pp[i][j] = p[j] * ww[i][j]
        pureIndex.append(np.argmax(pp[i]))
        maxPure.append(pp[i][pureIndex[i]])
    compSpec = np.zeros((numComps, nRow))
    for i in range(numComps):
        compSpecIndex = pureIndex[i]
        compSpec[i] = vuvMat.T[compSpecIndex]
    startSpecMat = np.zeros((numComps, nRow))
    for i in range(numComps):
        λ = compSpec.conj()[i]
        startSpecMat[i] = λ / np.sqrt(sum(λ*λ))
    startSpec = startSpecMat.T
    return startSpec


def cls(vuvArray, startCond):
    '''
    Takes in a matrix of size [m, n] and a second matrix of size [i, m], if the
    matrices are inverted, attempts to correct this, but one side of the first
    matrix must equal one side of the second matrix.

    Returns a matrix of size [i, n] corresponding to the solved components.

    Classical least squares calibration forces a fit to the known data, using
    the provided starting conditions (or spectra). If the starting conditions/
    spectra are of high quality (i.e., from a library or high-purity
    measurement) the results of CLS may be more accurate and faster than ALS.
    '''
    # Checks for data shape for future matrix operations.
    vaRow, vaCol = vuvArray.shape
    scRow, scCol = startCond.shape
    if scRow > scCol:
        startCond = startCond.T
        scRow, scCol = startCond.shape
    if scCol != vaRow:
        vuvArray = vuvArray.T
        vaRow, vaCol = vuvArray.shape
    if scCol != vaRow:
        raise ValueError('Dimensions of the matrices do not align!')
    numComps = scRow

    # Populates a zero-filled array with the results of the CLS.
    concentration = np.zeros((vaCol, numComps))
    for i in range(vaCol):
        tmp = np.linalg.inv(startCond @ startCond.T)
        c = (tmp @ startCond) @ vuvArray[:, i]
        concentration[i] = c

    # Normalization of results, so that the height of the data is 1.
    compSums = np.sum(startCond, axis=1)
    rawResults = np.array(concentration).T
    processedResults = np.ones_like(rawResults)
    for i, comp in enumerate(compSums):
        wavelengthFactor = np.sum(startCond[i])/np.sum(startCond)
        processedResults[i] = rawResults[i] * wavelengthFactor
    normalizationFactor = np.max(np.sum(processedResults, axis=0))
    results = processedResults / normalizationFactor
    return results


def als(vuvArray, startCond, Meta=None, numIter=100, convSigma=0.00):
    """
    The alternating least squares method iterates, given starting conditions,
    to attempt to converge on a solution. Performance and results depend
    greatly on the quality of data and starting conditions.
    """
    # Gets the shapes of the data/starting conditions, infers the number of
    # components, reshapes the array if necessary, and sets up a future if/
    # else statement
    vaRow, vaCol = vuvArray.shape
    scRow, scCol = startCond.shape
    # Setting up switches for differing shapes/spectra/chromatograms
    if scRow == vaRow:
        numComps = scCol
        ils = 1
    elif scCol == vaRow:
        numComps = scRow
        ils = 1
        startCond = startCond.conj().T
    elif scCol == vaCol:
        numComps = scRow
        ils = 2
    elif scRow == vaCol:
        numComps = scCol
        ils = 2
        startCond = startCond.conj().T
    else:
        raise ValueError('Matrices do not align!')
    if ils == 1:
        conc = startCond
        vaRow, numComps = conc.shape
        absorb = np.linalg.lstsq(conc, vuvArray)[0]
    elif ils == 2:
        absorb = startCond
        numComps, vaCol = absorb.shape
        conc = np.linalg.lstsq(absorb.T, vuvArray.T)[0]
    # Calculating the difference between the pcaMat and the vuvArray
    u, s, v = np.linalg.svd(vuvArray, 0)
    u = u[:, 0:numComps]
    s = np.diag(s[:numComps])
    v = v[0:numComps]
    pcaMat = u.dot(s).dot(v)
    # Matlab ALS calculates a few more numbers here, but I'm opting not to.
    # (They include a printout of the initial match/CPU time - unnecessary)
    sstn = np.sum(vuvArray * vuvArray)
    sigma2 = np.sqrt(sstn)
    divCount = 0
    # Main iteration loop
    for iterCount in range(numIter):
        if Meta:
            Meta['Progress'] = iterCount / numIter * 100
        # Estimate concentrations of the ALS solutions.
        conc = np.linalg.lstsq(absorb.T, pcaMat.T)[0].T
        # Non-negativity constraints
        conc2 = conc
        for i in range(vaRow):
            tmp1 = absorb @ absorb.conj().T
            tmp2 = absorb @ vuvArray[i, :].conj().T
            nnls = optimize.nnls(tmp1, tmp2)[0]
            conc2[i, :] = nnls.conj().T
        conc = conc2
        absorb = np.linalg.lstsq(conc, vuvArray)[0]
        absorb2 = absorb
        for i in range(vaCol):
            tmp1 = conc.conj().T @ conc
            tmp2 = conc.conj().T @ vuvArray[:,i]
            nnls = optimize.nnls(tmp1, tmp2)[0]
            absorb2[:, i] = nnls
        absorb = absorb2
        res = vuvArray - conc @ absorb
        u = np.sum(res*res)
        sigma = np.sqrt(u / vaRow * vaCol)
        change = (sigma2 - sigma) / sigma
        if change < 0.0:
            # print('Fitting isn\'t improving.')
            divCount += 1
        else:
            # print('Fitting is improving.')
            divCount = 0
        if change > 0 or iterCount == 1:
            sigma2 = sigma
            copt = conc
            sopt = absorb
        if np.abs(change) < convSigma:
            # print('Convergence is achieved.')
            return sopt.conj(), copt.T
        elif divCount > 20:
            # print('Diverging for >20 iterations, exiting.')
            return sopt.conj(), copt.T
    # print('Iterations exceeded allowed.')
    return sopt.conj(), copt.T


def getlibrary():
    root = tkinter.Tk()
    root.withdraw()
    getfile = tkinter.filedialog.askopenfilename
    libPath = getfile()
    with open('{}'.format(libPath)) as libObject:
        library = json.load(libObject)
    return(library)


def r2calc(xMeas, yMeas, xRef, yRef):
    """Calculates the R-squared value for two vectors"""
    # =========================================================================
    # If the number of y points in the measured and reference vectors are not
    # equivalent, iterpolates the measured vector to have the same number of
    # data points as the reference spectra.
    # =========================================================================
    if len(yMeas) != len(yRef):
        interpolate = scipy.interpolate.interp1d
        yMeas = interpolate(xMeas, yMeas, kind='linear',
                            fill_value='extrapolate')(xRef)
    # =========================================================================
    # Produces a correlation coefficient matrix of the y values.
    # =========================================================================
    rMatrix = np.corrcoef(yMeas, yRef)
    r2 = rMatrix[0][1] ** 2
    return r2


def searchspectra(vSpecX, vSpecY, library, returnList=True):
    results = []
    for name in library:
        spectra = library[name]['VUV Data']
        xVals = spectra[0]
        yVals = spectra[1]
        r2 = r2calc(vSpecX, vSpecY, xVals, yVals)
        results.append((name, r2))
    results.sort(key=lambda x: x[1], reverse=True)
    print(results[0], len(results))
    if returnList:
        return results
    else:
        topResult = results[0][0]
        topResultR2 = results[0][1]
        topResultData = library[topResult]['VUV Data']
        return topResult, topResultR2, topResultData


def interpolatespectra(xBad, yBad, xGood):
    if (len(xBad) != len(yBad)):
        raise ValueError('Data does not align!')
    elif len(xBad) != len(xGood):
        yNew = scipy.interpolate.interp1d(xBad, yBad, kind='linear',
                                          fill_value='extrapolate')(xGood)
        return yNew


def extractvuv(vuvFile, startWave=125, endWave=240, startTime=0, endTime=600):
    '''
    Connects to the provided VUV file (a .db, database file) via sqlite,
    extracts the data, crops it, and returns three numpy arrays of the time
    points, the wavelength points, and the data matrix that corresponds to the
    time points and wavelength points. User will be prompted for other
    parameters if they are not provided.
    '''
    conn = sqlite3.connect(vuvFile)
    c = conn.cursor()
    c.execute("SELECT * FROM {}".format('WL_Names'))
    rawλs = c.fetchall()[0][0]
    c.execute('SELECT {} FROM {}'.format('Time', 'Scan'))
    rawTimes = c.fetchall()
    c.execute("SELECT {} FROM {}".format('ABS', 'Scan'))
    rawArray = c.fetchall()
    conn.close()
    print('324')
    # =========================================================================
    # Unpacks the raw data and interpolates any problematic (nan/inf) points.
    # The '~' invertes the boolean matrix/mask.
    # =========================================================================
    unpackedTimes = np.array([time[0] for time in rawTimes])
    unpackedλs = np.array([struct.unpack('>f', rawλs[num:num+4])[0]
                          for num in range(0, len(rawλs), 4)])
    unpackedArray = np.zeros([len(rawArray), len(unpackedλs)], dtype='>f')
    for row, data in enumerate(rawArray):
        points = [struct.unpack('>f', data[0][num:num+4])
                  for num in range(0, len(data[0]), 4)]
        unpackedArray[row] = np.array(points).T
    mask = (np.isnan(unpackedArray) + np.isinf(unpackedArray))
    unpackedArray[mask] = np.interp(np.flatnonzero(mask),
                                    np.flatnonzero(~mask),
                                    unpackedArray[~mask])
    startλIndex = len(np.where(unpackedλs <= startWave)[0])
    endλIndex = len(np.where(unpackedλs <= endWave)[0])
    startTimeIndex = len(np.where(unpackedTimes <= startTime)[0])
    endTimeIndex = len(np.where(unpackedTimes <= endTime)[0]) + 1
    # =========================================================================
    # The axis lists and main data array are cropped and returned.
    # =========================================================================
    print('wave = ', len(unpackedλs), 'times = ', len(unpackedTimes))
    print(startλIndex, endλIndex, startTimeIndex, endTimeIndex)

    λPts = np.array(unpackedλs[startλIndex:endλIndex])
    timePts = unpackedTimes[startTimeIndex:endTimeIndex]
    trimmedArray = unpackedArray[startTimeIndex:endTimeIndex].T
    vuvArray = trimmedArray[startλIndex:endλIndex]
    print(vuvArray.shape)
    return timePts, λPts, vuvArray