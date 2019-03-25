import math
import sys

training = open(sys.argv[1], "r").read().split()
heldout = open(sys.argv[2], "r").read().split()
test = open(sys.argv[3], "r").read().split()
goodbad = open(sys.argv[4], "r").read().split()

def uni_model(doc, a):
    counts = {}
    for t in doc:
        if t in counts:
            counts[t] += 1
        else:
            counts[t] = 1

    num_types = len(counts)
    counts['*U*'] = 0
    num_tokens = len(doc)
    prob_dist = {}
    for c in counts:
        prob_dist[c] = (counts[c] + a)/float(num_tokens + a * num_types)

    return prob_dist

def log_prob(model, doc):
    prob = 1
    for d in doc:
        try:
            prob *= model[d]
        except KeyError:
            prob *= model['*U*']
    return math.log(prob)

print log_prob(uni_model(d, 1), test)
