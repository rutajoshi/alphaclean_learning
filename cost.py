"""
Handles cost estimation
"""
import copy

class CostEstimator(object):

    def __init__(self, rules, relation):

        self.rules = rules

        self.relation = relation

        self.currBest = relation

        self.currMaps = []


    def estimate(self, mapping):

        testRel = self.testAll(mapping)

        totalCost = 0.0
        for rule in self.rules:
            totalCost += rule.score(testRel)

        return totalCost, mapping, testRel


    def update(self, mapping, result):
        self.currBest = result
        self.currMaps.append(mapping)


    def _evalPredicate(self, pred, r):

        for i in pred:
            if r[i[0]] != i[1]:
                return False

        return True


    def _evalMapping(self, mapping, r):

        rCopy = list(r)

        if self._evalPredicate(mapping[0],r):
            rCopy[mapping[1]] = mapping[2]

        return tuple(rCopy)


    def testAll(self, mapping):

        relCopy = copy.copy(self.currBest)

        for r in relCopy:
            relCopy[r] = self._evalMapping(mapping, relCopy[r])

        return relCopy


