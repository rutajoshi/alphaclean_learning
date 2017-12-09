"""
Module defines a wrapper for a rule
"""

import inspect
import itertools

class Rule(object):


    def __init__(self, definition, distance=None, scope=None):

        self.definition = definition

        self.arity = len(inspect.getargspec(definition).args)


        if distance == None:
            self.distance = lambda s,t: len([ 1 for i,v in enumerate(s) if v != t[i]])
        else:
            self.distance = distance

        #what columns are touched
        self.scope = scope


    def score(self,relation):
        return len(self._getViolationStatistics(relation))
        
    
    def powerset(self,iterable):
        "list(powerset([1,2,3])) --> [(), (1,), (2,), (3,), (1,2), (1,3), (2,3), (1,2,3)]"
        s = list(iterable)
        return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(1,len(s)+1))


    def _getViolationTuples(self, relation):

        scanned = set()

        for element in itertools.product(relation,repeat=self.arity):

            #remove duplicates
            if len(element) != len(set(element)):
                continue

            #remove previously scanned
            if tuple(set(element)) in scanned:
                continue

            #add to the scanned list
            scanned.add(tuple(set(element)))

            arglist = [relation[key] for key in element]

            if not self.definition(*arglist):
                yield element



    def _getViolationStatistics(self, relation):

        violation_statistics = {}

        for vt in self._getViolationTuples(relation):

            for key in vt:
                if key not in violation_statistics:
                    violation_statistics[key] = 0

                violation_statistics[key] += 1

        return violation_statistics


    def _getCandidateViolations(self, relation):

        stats = self._getViolationStatistics(relation)

        violatingKeys = set()

        for vt in self._getViolationTuples(relation):

            violates = sorted([(stats[key],key) for key in vt],reverse=True)

            violatingKeys.add(violates[0][1])

        return violatingKeys



    def _getNNKey(self, key, violatingKeys, relation):
        
        nnList = sorted([(self.distance(relation[key], relation[comp]), comp) for comp in relation if comp not in violatingKeys])
        
        return nnList[0][1]


    def _getNNFix(self, relation):

        violatingKeys = self._getCandidateViolations(relation)


        if self.scope != None:
            scope = self.scope
        else:
            keylist = list(relation.keys())
            scope = range(0,len(relation[keylist[0]]))


        for key in violatingKeys:

            cleanComp = self._getNNKey(key, violatingKeys, relation)

            for pred in self.powerset(scope):

                literalsDirty = [relation[key][vp] for vp in pred]
                
                for target in scope:
                    yield (tuple(zip(pred, literalsDirty)), target ,relation[cleanComp][target])




