import datamanipulation
import numpy
import math
import random

def getPCAStuff(data, attributes):
    print ("data point count: " + str(len(data)))
    output = dict()

    centerData = True

    datMan = datamanipulation.DataManipulation(attributes)

    mean = datMan.vectorMean(data)
    standardDeviation = datMan.standardDeviation(data)

    output['means'] = mean

    # center data
    if centerData:
        for d in data:
            d["Country_OG"] = d["Country"]
            d["Year_OG"] = d["Year"]
            d["Region_OG"] = d["Region"]
            d["Income Group_OG"] = d["Income Group"]
            for a in attributes:
                try:
                    d[a] = d[a] - mean[a]
                except TypeError:
                    d[a] = -1

    standardizeData = False
    # standardize data
    if standardizeData:
        for d in data:
            for a in attributes:
                if d[a] != -1 and standardDeviation[a] != 0:
                    d[a] /= standardDeviation[a]

    covNumPointsUsed = dict()

    # generate covariance matrix
    C = dict()
    cov_mat = numpy.zeros(shape=(len(attributes), len(attributes)))
    for ii, i in enumerate(attributes):
        C[i] = dict()
        covNumPointsUsed[i] = dict()
        for ji, j in enumerate(attributes):
            # remove no-entry values in i and j from data
            reducedData = [d for d in data if d[i] != -1 and d[j] != -1]
            covNumPointsUsed[i][j] = len(reducedData)
            if len(reducedData) <= 1:
                C[i][j] = 0
            else:
                C[i][j] = sum([d[i] * d[j] for d in reducedData]) / float(len(reducedData) - 1)
            cov_mat[ii][ji] = C[i][j]

    output['covmat'] = C
    output['covNumPointsUsed'] = covNumPointsUsed

    # generate correlateion matrix
    R = dict()
    corr_mat = numpy.zeros(shape=(len(attributes), len(attributes)))
    for ii, i in enumerate(attributes):
        R[i] = dict()
        for ji, j in enumerate(attributes):
            if C[i][i] == 0 or C[j][j] == 0:
                R[i][j] = 0
            else:
                R[i][j] = C[i][j] / math.sqrt(C[i][i] * C[j][j])
            corr_mat[ii][ji] = R[i][j]

    output['corrmat'] = R

    # generate eigenvectors/values
    eig_vals, eig_vecs = numpy.linalg.eig(corr_mat)
    eig_vals = [e.real if isinstance(e, complex) else e for e in eig_vals]
    
    trace = sum(eig_vals)
    output['trace'] = trace

    # organize eigenvectors into desired format
    eigenvectors = []
    for ei in range(len(eig_vecs)):
        eigenvector = dict()
        for ai, a in enumerate(attributes):
            vecval = eig_vecs[ei][ai]
            eigenvector[a] = vecval.real if isinstance(vecval, complex) else vecval
        eigenvector['_eigenvalue'] = eig_vals[ei]
        eigenvector['_perc_variance'] = eig_vals[ei] / trace
        eigenvectors.append(eigenvector)
    eigenvectors.sort(key = lambda e: e['_eigenvalue'], reverse=True)

    # throw out eigenvectors with very small percent variance (but keep at least 2)
    eigenvectors = [e for ei, e in enumerate(eigenvectors) if ei < 2 or e['_perc_variance'] >= .01]
    output['eigenvectors'] = eigenvectors

    # generate sum of squared loadings (significance)
    significance = dict()
    for a in attributes:
        sigSum = 0
        for v in eigenvectors:
            sigSum += (v[a] ** 2) * v['_perc_variance']
        significance[a] = sigSum
    output['significance'] = significance

    # calculate data projected onto PCA vectors
    scored_data = []
    for d in data:
        el = dict()
        for ei, e in enumerate(eigenvectors):
            el[ei] = sum([e[a] * d[a] for a in attributes])
        el["Country"] = d["Country_OG"]
        el["Year"] = d["Year_OG"]
        el["Region"] = d["Region_OG"]
        el["Income Group"] = d["Income Group_OG"]
        scored_data.append(el)
    output['scored_data'] = scored_data

    return output