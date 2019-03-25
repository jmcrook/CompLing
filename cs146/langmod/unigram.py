import math
import sys

training = ("$TOPSYMBOL ".join(open(sys.argv[1], "r").read().split('\n'))).split()
heldout = ("$TOPSYMBOL ".join(open(sys.argv[2], "r").read().split('\n'))).split()
test = ("$TOPSYMBOL ".join(open(sys.argv[3], "r").read().split('\n'))).split()
goodbad = (" $TOPSYMBOL\n$TOPSYMBOL ".join(('\n' + open(sys.argv[4], "r").read()).split('\n'))).split('\n')[1:]


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

gr=(math.sqrt(5)-1)/2
def gss(f,a,b,tol=1e-5):
    '''
    golden section search
    to find the minimum of f on [a,b]
    f: a strictly unimodal function on [a,b]

    example:
    >>> f=lambda x:(x-2)**2
    >>> x=gss(f,1,5)
    >>> x
    2.000009644875678

    '''
    c=b-gr*(b-a)
    d=a+gr*(b-a)
    while abs(c-d)>tol:       
        fc=f(c);fd=f(d)
        if fc<fd:
            b=d
            d=c  #fd=fc;fc=f(c)
            c=b-gr*(b-a)
        else:
            a=c
            c=d  #fc=fd;fd=f(d)
            d=a+gr*(b-a)
    return (b+a)/2


def log_prob(model, doc):
    prob = 0
    for d in doc:
        try:
            prob += math.log(model[d])
        except KeyError:
            prob += math.log(model['*U*'])
    return -prob


def log_prob_func(alp):
    return log_prob(uni_model(training, alp), heldout)


gb_pairs = [(goodbad[2*i].split(), goodbad[2*i + 1].split()) for i in range(len(goodbad)/2)]

def check_gb(gbp, model):

    correct = 0
    for p in gbp:
        if log_prob(model, p[0]) < log_prob(model, p[1]):
            correct += 1
    return correct/float(len(gbp))


print log_prob(uni_model(training, 1), test)

optimal_alpha = gss(log_prob_func, 0, 30)

print log_prob(uni_model(training, optimal_alpha), test)

print 100 * check_gb(gb_pairs, uni_model(training, optimal_alpha))

print optimal_alpha










