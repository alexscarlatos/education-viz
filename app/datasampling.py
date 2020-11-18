import csv
import random
import math
import re
import copy
import datamanipulation

initial_data = []
attributes = []

# generates random data set
def createRandomData(size, data_min, data_max):
    global initial_data
    global attributes
    initial_data = []
    attributes = ['x','y']
    
    for i in range(0, size):
        el = dict()
        for a in attributes:
            el[a] = random.randint(data_min, data_max)
        initial_data.append(el)

# generates random data set with y=x slope
def createRandomDiagonalData(data_min, data_max):
    global initial_data
    global attributes
    initial_data = []
    attributes = ['x','y']

    for i in range(data_min, data_max):
        el = dict()
        for a in attributes:
            el[a] = i + random.randint(-5, 5)
        initial_data.append(el)

# generates random data in outer 4 corners
def createRandomQuadData(size, data_min, data_max):
    global initial_data
    global attributes
    initial_data = []
    attributes = ['x','y']

    dr = data_max - data_min

    for i in range(0, int(size/4)):
        el = dict()
        el['x'] = random.randint(data_min, data_max - int(dr * 3 / 4))
        el['y'] = random.randint(data_min, data_max - int(dr * 3 / 4))
        initial_data.append(el)
    for i in range(0, int(size/4)):
        el = dict()
        el['x'] = random.randint(data_min, data_max - int(dr * 3 / 4))
        el['y'] = random.randint(data_min + int(dr * 3 / 4), data_max)
        initial_data.append(el)
    for i in range(0, 5):
        el = dict()
        el['x'] = random.randint(data_min + int(dr * 3 / 4), data_max)
        el['y'] = random.randint(data_min, data_max - int(dr * 3 / 4))
        initial_data.append(el)
    for i in range(0, int(size/4)):
        el = dict()
        el['x'] = random.randint(data_min + int(dr * 3 / 4), data_max)
        el['y'] = random.randint(data_min + int(dr * 3 / 4), data_max)
        initial_data.append(el)

def formatString(s):
    return re.sub(r'[^\w.]', '', s)

# imports data from given csv file
def importData(filename):
    global initial_data
    global attributes
    initial_data = []
    attributes = []

    with open("data/" + filename) as datafile:
        csvReader = csv.reader(datafile, quotechar='"')
        first = True
        for cols in csvReader:
            if first:
                first = False
                for c in cols:
                    #attributes.append(formatString(c))
                    attributes.append(c)
            else:
                el = dict()
                i = 0
                for c in cols:
                    #val = formatString(c)
                    val = c
                    #if val == "":
                    #    val = 0
                    try:
                        val = float(val)
                    except ValueError:
                        pass
                    finally:
                        el[attributes[i]] = val
                    i += 1
                    if i >= len(attributes):
                        break
                initial_data.append(el)

# get a random sample from the given data of the given size
# note: elements added to random sample are removed from data
def getRandomSample(data, sampleSize):
    datMan = datamanipulation.DataManipulation(attributes)

    downSampledData = []
    n = len(data)

    for k in range(0, sampleSize):
        el = data[random.randint(0, n - k - 1)]
        data.remove(el)
        downSampledData.append(el)
    downSampledData.sort(key=lambda d: datMan.mag(d))

    return downSampledData

# return a random sampling of the given dataset of the given size
def randomSampling(data, sampleSize):
    print("Random Sampling...")
    if sampleSize > 0:
        keptData = getRandomSample(data, sampleSize)
        for el in data:
            el['kept'] = False
        for el in keptData:
            el['kept'] = True
        return data + keptData
    else:
        for el in data:
            el['kept'] = True
        return data

# returns if given value can be cast to a float
def floatOr0(val):
    try:
        return float(val)
    except:
        return 0

# generate clusters and sample appropriate amount from each cluster
# return sampled dataset along with clustering info
def stratifiedSampling(data, sampleSize, max_k, elbow_ratio_cutoff):
    print("Clustering...")

    datMan = datamanipulation.DataManipulation(attributes)

    # get data range
    data_min = dict()
    data_max = dict()
    for a in attributes:
        data_min[a] = min([floatOr0(d[a]) for d in data])
        data_max[a] = max([floatOr0(d[a]) for d in data])

    output = dict()

    num_optimization_tries = 4 # number of times to try each k to find an optimal positioning
    max_update_iterations = 6 # max number of times to update each k-point to find associated points

    best_attempts = [] # maps k to the best clustering found for k clusters
    optimal_k = max_k - 1 # default optimal k if elbow is never found

    # iterate through k until an optimal clustering is found
    for k in range(1, max_k + 1):
        print ("k = " + str(k))
        # run calculations several times and keep the best outcome
        best_attempt = dict()
        best_mse = -1

        # run algorithm several times for each k
        for opt_try in range(0, num_optimization_tries):
            # initialize random k-means
            k_means = []
            for ki in range(0, k):
                mean = dict()
                for a in attributes:
                    mean[a] = random.randint(int(data_min[a]), int(data_max[a]))
                k_means.append(mean)
            k_means.sort(key=lambda km: datMan.mag(km))

            # assign data points to k-points and repeat until optimal (or timeout)
            cluster_elements = [0] * k # maps k to elements in that cluster
            for update_it in range(0, max_update_iterations):
                best_ks = [] # maps data element index to its closest k
                optimal = True # if this iteration is optimal (all the k-points match their clusters' means)
                this_attempt = dict()

                # find the closest k to each data element
                for i in range(0, len(data)):
                    el = data[i]
                    best_k = 0
                    best_dist = -1
                    for ki in range(0, k):
                        dist = datMan.euclidianDist(el, k_means[ki])
                        if best_dist < 0 or dist < best_dist:
                            best_dist = dist
                            best_k = ki
                    best_ks.append(best_k)

                # calculate actual mean of each cluster and update k-means if necessary
                for ki in range(0, k):
                    # get this cluster's elements and get the mean
                    cluster_elements[ki] = [data[i] for i, k_val in enumerate(best_ks) if k_val == ki]
                    mean = datMan.vectorMean(cluster_elements[ki])
                    if mean == None:
                        mean = k_means[ki]
                    line = "k-mean: " + str(k_means[ki]) + " elements: " + str(cluster_elements[ki]) + " actual mean: " + str(mean) + " "
                    # check if this k-point is equal to its cluster's mean
                    optimal = optimal and k_means[ki] == mean
                    # set k-means to the actual means of their clusters
                    k_means[ki] = mean
                
                # no need to update when k-points match their cluster means
                if optimal == True:
                    break

            # calculate MSE for this k-clustering
            mse = 0
            for ki in range(0, k):
                # sum of squared distances of data points to their k-point in each cluster
                mse += sum([datMan.euclidianDist(k_means[ki], el) ** 2 for el in cluster_elements[ki]])
            mse /= float(len(data))

            # record the attempt with the lowest mse
            this_attempt['mse'] = mse
            this_attempt['kmeans'] = k_means
            this_attempt['clusterelements'] = cluster_elements
            if best_mse < 0 or mse < best_mse:
                best_attempt = copy.deepcopy(this_attempt)
                best_mse = mse
        
        best_attempts.append(best_attempt)

        # see if an elbow exists at the k before this one
        if k > 2:
            dif1 = best_attempts[k - 3]['mse'] - best_attempts[k - 2]['mse']
            dif2 = best_attempts[k - 2]['mse'] - best_attempt['mse']
            if dif2 / dif1 < elbow_ratio_cutoff:
                optimal_k = k - 2
                break

    final_clustering = best_attempts[optimal_k]
    final_clustering['sampledelements'] = []

    # sample an appropriate amount of data points from each cluster
    print("Sampling on clusters...")
    if sampleSize <= 0:
        sampleSize = len(data)
    for ki in range(0, optimal_k + 1):
        cluster_elements = final_clustering['clusterelements'][ki]
        cluster_weight = float(len(cluster_elements)) / float(len(data))
        final_clustering['sampledelements'].append(getRandomSample(cluster_elements, math.ceil(cluster_weight * sampleSize)))

    # prepare data for output
    datapoints = []
    for ki, c in enumerate(final_clustering['clusterelements']):
        for el in c:
            el['kcluster'] = ki
            el['kept'] = False
            datapoints.append(el)
    for ki, c in enumerate(final_clustering['sampledelements']):
        for el in c:
            el['kcluster'] = ki
            el['kept'] = True
            datapoints.append(el)
    output['datapoints'] = datapoints
    output['kmeans'] = final_clustering['kmeans']
    output['MSE'] = [a['mse'] for a in best_attempts]

    return output