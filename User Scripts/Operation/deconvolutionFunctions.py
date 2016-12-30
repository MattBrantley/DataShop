# coding=utf-8
import numpy as np


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