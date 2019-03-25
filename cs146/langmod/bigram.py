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

    num_types = len(counts) + 1
    counts['*U*'] = 0
    num_tokens = len(doc)
    prob_dist = {}
    for c in counts:
        prob_dist[c] = (counts[c] + a)/float(num_tokens + a * num_types)

    return prob_dist


def bi_model(doc, uni_m, b):

    n_ww = {}
    n_wo = {}

    for t in range(len(doc) - 1):
        bigram = tuple(doc[t:t+2])
        if bigram in n_ww:
            n_ww[bigram] += 1
        else:
            n_ww[bigram] = 1
            
    for ww in n_ww:
        if ww[0] in n_wo:
            n_wo[ww[0]] += n_ww[ww]
        else:
            n_wo[ww[0]] = n_ww[ww]

    n_ww[('*U*','*U*')] = 0
    n_wo[('*U*')] = 0

    for w in set(doc):
        n_ww[(w ,'*U*')] = 0
        n_ww[('*U*', w)] = 0

    prob_dist = {}

    for ww in n_ww:
        prob_dist[ww] = ((float(n_ww[ww]) + (float(b) * uni_m[ww[1]]))
                        /(float(n_wo[ww[0]]) + float(b)))

    return prob_dist


def log_prob2(model, doc):
    prob = 0
    for d in range(len(doc) - 1):
        try:
            prob += math.log(model[tuple(doc[d:d+2])])
        except KeyError:
            try:
                prob += math.log(model[(doc[d],'*U*')])
            except KeyError:
                try:
                    prob += math.log(model[('*U*', doc[d+1])])
                except KeyError:
                    prob += math.log(model[('*U*','*U*')])

    return -prob


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


def check_gb(gbp, model):

    correct = 0
    for p in gbp:
        if log_prob(model, p[0]) < log_prob(model, p[1]):
            correct += 1
    return correct/float(len(gbp))

def log_prob1(model, doc):
    prob = 0
    for d in doc:
        try:
            prob += math.log(model[d])
        except KeyError:
            prob += math.log(model['*U*'])
    return -prob


def log_prob_func1(alp):
    return log_prob1(uni_model(training, alp), heldout)


optimal_alpha = gss(log_prob_func1, 0, 100)
uni = uni_model(training, optimal_alpha)
uni_1 = uni_model(training, 1)

def log_prob_func2(bet):
    return log_prob2(bi_model(training, uni, bet), heldout)


def check_gb(gbp, model):

    correct = 0
    for p in gbp:
        if log_prob2(model, p[0]) < log_prob2(model, p[1]):
            correct += 1
    return correct/float(len(gbp))


optimal_beta =  gss(log_prob_func2, 0, 1000)
optimal_bi_model = bi_model(training, uni, optimal_beta)


print log_prob2(bi_model(training, uni_1, 1), test)
print log_prob2(optimal_bi_model, test)

gb_pairs = [(goodbad[2*i].split(), goodbad[2*i + 1].split()) for i in range(len(goodbad)/2)]

print 100 * check_gb(gb_pairs, optimal_bi_model)

print optimal_alpha
print optimal_beta












