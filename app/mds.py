import datamanipulation
import math
import numpy
from sklearn import manifold

def getMDSStuff(data, attributes):
    output = dict()

    datMan = datamanipulation.DataManipulation(attributes)

    mds = manifold.MDS(dissimilarity='precomputed')

    for d in data:
        for a in attributes:
            try:
                testfloat = float(d[a])
            except:
                d[a] = ""

    # get covariance of attributes
    n = len(attributes)
    cov = numpy.zeros(shape=(n,n))
    for ii, i in enumerate(attributes):
        for ji, j in enumerate(attributes):
            # remove no-entry values in i and j from data
            reducedData = [d for d in data if d[i] != "" and d[j] != ""]
            if len(reducedData) <= 1:
                cov[ii][ji] = 0
            else:
                cov[ii][ji] = sum([d[i] * d[j] for d in reducedData]) / float(len(reducedData) - 1)

    # get (1 - correlation) of attributes for distances
    corr = numpy.zeros(shape=(n,n))
    for i in range(n):
        for j in range(n):
            if cov[i][j] == 0:
                corr[i][j] = 0
            else:
                corr[i][j] = 1 - abs(cov[i][j] / math.sqrt(cov[i][i] * cov[j][j]))

    attpoints = mds.fit(corr).embedding_

    output['attributes'] = attpoints.tolist()

    return output