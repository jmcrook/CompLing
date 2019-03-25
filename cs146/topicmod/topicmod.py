import sys
import random
import numpy.random
import time
import math
start = time.time()

data = open(sys.argv[1], "r").read().split("\n")

## STEP 1 OF GIBBS SAMPLING ALGORITHM
docWordTopic = {} ## takes in word indices
docs = {}         ## keeps track of index <-> word
wordcounts = {}   ## takes in word strings
docTopicCount = {}
topicWordCount = {t: {} for t in range(50)} ## takes in word strings

n_do = {}
n_to = {t: 0 for t in range(50)}

alpha  = 0.5
C = 10
N = 50.0
V = 0.0  # 9935



currdoc = 0
## the first line of news1000.txt is blank
for l in data[1:]:
	line = l.split()
	if l[0] != " ":
		currdoc += 1.0
		docs[currdoc] = []

		## the number words with any topic in a doc is just the number o
		## of words in that doc
		n_do[currdoc] = float(line[0])

		##words recorded as indices
		docWordTopic[currdoc] = {i: 0 for i in range(int(n_do[currdoc]))}
		docTopicCount[currdoc] = {t: 0 for t in range(50)}

		currWord = 0.0
 	else:
 		for w in line:

 			docs[currdoc].append(w)
 			## initialize to random topic
 			t = random.randint(0, 49)  ## different from numpy.random

 			docWordTopic[currdoc][currWord] = t


 			n_to[t] += 1.0

 			if w not in wordcounts:
 				wordcounts[w] = 0.0
 				V += 1.0

 			wordcounts[w] += 1.0

 			docTopicCount[currdoc][t] += 1.0

 			if w not in topicWordCount[t]:
 				topicWordCount[t][w] = 1.0
 			else:
 				topicWordCount[t][w] += 1.0

 			currWord += 1.0

# print sum([docTopicCount[30][t] for t in docTopicCount[30]]) == len(docs[30])
# print len(topicWordCount) == 50
# print len(wordcounts) == 9935
# print sum([n_to[t] for t in n_to]) == sum([wordcounts[w] for w in wordcounts])

# true
# true
# true
# true


def getLikelihood():
	l = 0
	for d in docWordTopic:
		for w in docWordTopic[d]:
			t = docWordTopic[d][w]
			l += math.log(
				(docTopicCount[d][t] + alpha)/(n_do[d] + N*alpha) * 
				(topicWordCount[t][docs[d][w]] + alpha)/(n_to[t] + V*alpha))	
	return -l


oldLikelihood = getLikelihood()

converged = False

while not converged:
	#STEP A
	for d in docWordTopic:

		n_do[d] -= 1.0

		for w in docWordTopic[d]:

			word = docs[d][w] # get the actual word string

			#current word topic
			topic = docWordTopic[d][w]
			n_to[topic] -= 1.0

			# A.i

			docTopicCount[d][topic] -= 1.0
			topicWordCount[topic][word] -= 1.0


			# A.ii
			choice_arr = [0]* 50
			choice_sum = 0.0

			for t in range(50):
				ptd = (docTopicCount[d][t] + alpha)/(n_do[d] + N*alpha) 
				try:
					pwt = (topicWordCount[t][word] + alpha)/(n_to[t] + V*alpha) 
				except KeyError:
					pwt = (alpha)/(n_to[t] + V*alpha)

				choice_arr[t] = ptd*pwt
				choice_sum += ptd*pwt

			arr = [x/choice_sum for x in choice_arr] ## normalized choice array

			#A.iii
			newTopic = numpy.random.choice(50, p=arr)

			#A.iv
			docTopicCount[d][newTopic] += 1.0

			if word not in topicWordCount[newTopic]:
				topicWordCount[newTopic][word] = 0.0

			topicWordCount[newTopic][word] += 1.0
			docWordTopic[d][w] = newTopic

			n_to[newTopic] += 1.0

		n_do[d] += 1.0

	likelihood = getLikelihood()
	diff = 1.0 - float(likelihood)/oldLikelihood
	if diff < 0.01:
		converged = True
	else:
		oldLikelihood = likelihood



print "Negative log likelihood of data at convergence: ", getLikelihood()
print 
print "Topics for article 17, sorted by likelihood: "



topic_probs = []
for topic in docTopicCount[17]:
		topic_probs.append((docTopicCount[17][topic]/n_do[17], topic))


topic_probs.sort(reverse=True)
for s in topic_probs:
	print s

print 
print "Fifteen most probable words by topic:"
for t in topicWordCount:
	word_probs = []
	for w in topicWordCount[t]:
		pwt = (topicWordCount[t][w] + 5.0)/(wordcounts[w] + N*5)
		word_probs.append((pwt,w))


	word_probs.sort(reverse=True)
	print "TOPIC ", t
	for s in word_probs[:15]:
		print "          ", s[1]
