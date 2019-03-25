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
		#print "iteration: " + str(i)

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

ftrain = open(sys.argv[1], "r").read() #.split('\n')
etrain = open(sys.argv[2], "r").read() #.split('\n')
ftest = open(sys.argv[3], "r").read().split('\n')




#P(e|f) = tau[f][e]
tau_fe = EM(ftrain, etrain, 10)

#decoding
# getting argmax p(e|f) for each f in a given sentence

#dumb_out = open("/gpfs/main/home/jcrook/course/cs146/mt/dumb_out.txt", "w")

for i in range(len(ftest)):
	fsent = ftest[i].split()
	f_to_e_trans = []

	for fword in fsent:
		if fword in tau_fe:
			found_possible = False
			for e in tau_fe[fword]:
				if not found_possible:
					best_e = e
					found_possible = True
				else:
					if tau_fe[fword][e] > tau_fe[fword][best_e]:
						best_e = e
			f_to_e_trans.append(best_e)
		else:
			f_to_e_trans.append(fword)
	#dumb_out.write(" ".join(f_to_e_trans) + "\n")
	print " ".join(f_to_e_trans)

#dumb_out.close()









