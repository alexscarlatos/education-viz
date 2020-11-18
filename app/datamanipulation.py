import math

class DataManipulation:
    def __init__(self, attributes):
        self.attributes = attributes

    # return the Euclidian distance of 2 given points, represented as dicts
    def euclidianDist(self, p1, p2):
        sum = 0
        for a in self.attributes:
            try:
                sum += (p1[a] - p2[a]) ** 2
            except TypeError:
                pass
        return math.sqrt(sum)

    # return the magnitude of a given vector, represented as a dict
    def mag(self, v):
        sum = 0
        for a in self.attributes:
            try:
                sum += v[a] ** 2
            except TypeError:
                pass
        return math.sqrt(sum)

    # returns the mean of a list of vectors, represented as dicts
    def vectorMean(self, vectors):
        if len(vectors) == 0:
            return None

        sum = dict()
        for a in self.attributes:
            sum[a] = 0
            for v in vectors:
                try:
                    sum[a] += v[a]
                except TypeError:
                    pass
            sum[a] /= len(vectors)
        return sum

    # returns the standard deviation of a list of vectors, represented as dicts
    def standardDeviation(self, vectors):
        if len(vectors) == 0:
            return None
        
        standardDeviation = dict()
        means = self.vectorMean(vectors)
        for a in self.attributes:
            attSum = 0
            for v in vectors:
                try:
                    attSum += (v[a] - means[a]) ** 2
                except TypeError:
                    pass
            standardDeviation[a] = math.sqrt(attSum / float(len(vectors) - 1))
        return standardDeviation