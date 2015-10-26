from numpy import matrix
from fractions import Fraction
from random import random

# We assume that the index 0 is state 1, index 1 is state 2, etc.
class HiddenMarkovModel(object):
    def __init__(self, mu, p, q):
        self.mu = mu
        self.p = p
        self.q = q

    def calculateYPermutation(self, yPerm):
        n = len(yPerm)
        # Generate all x permutations
        def generatePermutation(n, numStates, currPerm = [], acc = []):
            if len(currPerm) == numStates:
                return [currPerm]
            for i in range(1, numStates + 1):
                acc += generatePermutation(n, numStates, currPerm + [i], [])
            return acc
        xPerms = generatePermutation(len(yPerm), int(p.shape[0]))
        result = 0
        for perm in xPerms:
            component = mu.item(perm[0] - 1)
            for i in range(len(perm) - 1):
                component *= p.item(perm[i] - 1, perm[i+1] - 1)
            for i in range(len(perm)):
                component *= p.item(perm[i] - 1, yPerm[i] - 1)
            result += component
        return float(result)

    def yStatesUpTo(self, n):
        xStates = self.xStatesUpTo(n)
        yStates = []
        for x in xStates:
            yVec = matrix([[q.item(x - 1, 0), q.item(x-1, 1)]])
            yStates.append(self.discreteInverse(yVec))
        return yStates

    def xStatesUpTo(self, n):
        states = [self.discreteInverse(mu)]
        currPtm = None
        for i in range(1, n + 1):
            # First time through the loop
            if currPtm is None:
                currPtm = p
            else:
                currPtm *= p
            v = mu * currPtm
            states.append(self.discreteInverse(v))
        return states

    def discreteInverse(self, vector):
        u = random()
        probStateList = [(vector.item(i), i+1) for i in range(int(vector.shape[1]))]
        probStateList.sort()
        probStateList = probStateList[::-1]
        accumulator = 0
        for frac, state in probStateList:
            accumulator += frac
            if u <= accumulator:
                return state

if __name__ == '__main__':
    mu = matrix([[Fraction(1, 6), Fraction(2,6), Fraction(3, 6)]])
    p = matrix([[Fraction(0,1), Fraction(2, 3), Fraction(1, 3)],
                [Fraction(1,3), Fraction(1,3), Fraction(1,3)],
                [Fraction(1,3), Fraction(2,3), Fraction(0,3)]])
    q = matrix([[Fraction(1,1), Fraction(0,1)],
                [Fraction(1,2), Fraction(1,2)],
                [Fraction(0,1), Fraction(1,1)]])
    hmm = HiddenMarkovModel(mu, p, q)
    # 3.1
    print hmm.xStatesUpTo(3)
    # 3.2
    print hmm.yStatesUpTo(3)
    # 3.3
    print hmm.calculateYPermutation([2,1,2])
