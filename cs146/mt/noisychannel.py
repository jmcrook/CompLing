import math
import sys
import time
#start_time = time.time()


# INPUT: two parallel corpora in lang1 and lang2, one sentence per line
#returns tau[l1][l2], the likelihood that word l1 is the translation of l2
#tau[e][f] is P(f|e)
def EM(l1_corpus, l2_corpus, num_iter):

    l1train = l1_corpus.split('\n')
    l2train = l2_corpus.split('\n')

    l1l2_pairs = [(("*n* " + l1train[i]).split(), l2train[i].split()) for i in range(len(l1train))]

    # l1Tokens = [w for s in l1train for w in s.split()]
    # l1Tokens.append("*n*")
    # l1Vocab = set(l1Tokens)

    # l2Tokens = [w for s in l2train for w in s.split()]


    # l2Vocab = set(l2Tokens)

    #initialize tau
    tau = {}
    for p in l1l2_pairs:
        l1sent = p[0]
        l2sent = p[1]
        for l1 in l1sent:
            if l1 not in tau:
                tau[l1] = {}
            for l2 in l2sent:
                if l2 not in tau[l1]:
                    tau[l1][l2] = 1.0

    for i in range(num_iter):
        print "iteration: " + str(i)

        n = {}

        for l1 in tau:
            n[l1] = {}
            for l2 in tau[l1]:
                n[l1][l2] = 0.0

        for p in l1l2_pairs:
            l1Sent = p[0]
            l2Sent = p[1]

            for l2 in l2Sent:
                pk = 0.0
                for l1 in l1Sent:
                    pk += tau[l1][l2]

                for l1 in l1Sent:
                    n[l1][l2] += tau[l1][l2]/pk

        for l1 in tau:
            n_l1 = 0.0
            for l2 in n[l1]:
                n_l1 += n[l1][l2]

            for l2 in tau[l1]:
                tau[l1][l2] = n[l1][l2]/n_l1

    return tau

def uni_model(doc, a):
    counts = {}
    for t in doc:
        if t in counts:
            counts[t] += 1
        else:
            counts[t] = 1

    num_types = len(counts) + 1 # for UNK
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


# takes in bigram of the form tuple(str1, str2)
def bgram_prob(model, bigram):
    try:
        prob = model[bigram]
    except KeyError:
        try:
            prob = model[(bigram[0],'*U*')]
        except KeyError:
            try:
                prob = model[('*U*', bigram[1])]
            except KeyError:
                prob = model[('*U*','*U*')]

    return prob


ftrain = open(sys.argv[1], "r").read() #.split('\n')
etrain = open(sys.argv[2], "r").read() #.split('\n')
ftest = open(sys.argv[3], "r").read().split('\n')

Ftrain = ftrain.split("\n")
Etrain = etrain.split("\n")

possible_e = {}

FE_pairs = [((Ftrain[i]).split(), ("*n* " + Etrain[i]).split()) for i in range(len(Ftrain))]

for p in FE_pairs:
    F_sent = p[0]
    E_sent = p[1]

    for f in F_sent:
        if f not in possible_e:
            possible_e[f] = []
        for e in E_sent:
            if e not in possible_e[f]:
                possible_e[f].append(e)



#e_senate_2 = open("/gpfs/main/home/jcrook/course/cs146/mt/english-senate-2.txt", "r").read().split("\n")


#P(f|e) = tau[e][f]
tau_ef = EM(etrain, ftrain, 10)

probable_e = {}

for f in possible_e:
    probable_e[f] = []
    for e in possible_e[f]:
        if tau_ef[e][f] > 0.05:
            probable_e[f].append(e)





english_tokens = [w for e_sent in etrain.split("\n") for w in ("*n* " + e_sent).split()]
english_model = bi_model(english_tokens, uni_model(english_tokens, 1.59), 110)

french_tokens = [w for f_sent in ftrain.split("\n") for w in (f_sent).split()]
french_types = set(french_tokens)

#noisyChannel_out = open("/gpfs/main/home/jcrook/course/cs146/mt/noisyChannel_out", "w")
#correct_out = open("/gpfs/main/home/jcrook/course/cs146/mt/correct_out", "w")

#translated_sentences_indices = []

for s in ftest:
    f_sent = s.split()
    prev = 0
    e_trans = ["*n*"]
    for fword in f_sent:
        if fword in french_types:
            found_possible = False
            for e in probable_e[fword]:       
                if not found_possible:
                    best_e = e
                    best_prob = bgram_prob(english_model, (e_trans[prev], best_e)) * tau_ef[best_e][fword]
                    found_possible = True
                else:
                    new_prob = bgram_prob(english_model, (e_trans[prev], e)) * tau_ef[e][fword] 
                    if new_prob > best_prob:
                        best_e = e
                        best_prob = new_prob
            e_trans.append(best_e)
        else:
            e_trans.append(fword)
        prev += 1
    print " ".join(e_trans[1:])
    #noisyChannel_out.write(" ".join(e_trans[1:]) + "\n")
    
#noisyChannel_out.close()

#for i in translated_sentences_indices:
 #   correct_out.write(e_senate_2[i] + "\n")

#correct_out.close()

# f = 0.551207708718


