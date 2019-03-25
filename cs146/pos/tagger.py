import sys

training = open(sys.argv[1], "r").read().split('\n')
testing = open(sys.argv[2], "r").read().split('\n')



tag1_tag2Counts = {}
tag1_word1Counts = {}

#GET COUNTS FOR TAU AND SIGMA
for line in training:
	i = 0
	lst = ["*STRT*", "*STRT*"] + line.split() + ["*END*", "*END*"]
	length = len(lst) - 2

	while i < length:
		word = lst[i]
		tag = lst[i+1]
		tag2 = lst[i+3]

		if tag not in tag1_word1Counts:
			tag1_word1Counts[tag] = {}

		if word not in tag1_word1Counts[tag]:
			tag1_word1Counts[tag][word] = 1
		else:
			tag1_word1Counts[tag][word] += 1



		if tag not in tag1_tag2Counts:
			tag1_tag2Counts[tag] = {}

		if tag2 not in tag1_tag2Counts[tag]:
			tag1_tag2Counts[tag][tag2] = 1
		else:
			tag1_tag2Counts[tag][tag2] += 1

		i += 2


#SMOOTH THE COUNTS

for tag in tag1_word1Counts:
	tag1_word1Counts[tag]["*UNK*"] = 1


#print tag1_word1Counts["VB"]["time"] # 2
#print tag1_word1Counts["NN"]["time"] # 745

tau_y1w1 = {}

tau_y1w1["*END*"] = {}
tau_y1w1["*END*"]["*END*"] = 1

sig_y1y2 = {}

#NORMALIZE THE COUNTS >> GET TAU AND SIGMA

for tag in tag1_tag2Counts:
	total = sum([tag1_tag2Counts[tag][c] for c in tag1_tag2Counts[tag]])

	sig_y1y2[tag] = {}

	for tag2 in tag1_tag2Counts[tag]:
		sig_y1y2[tag][tag2] = tag1_tag2Counts[tag][tag2]/float(total)

for tag in tag1_word1Counts:
	total = sum([tag1_word1Counts[tag][c] for c in tag1_word1Counts[tag]])

	tau_y1w1[tag] = {}

	for word in tag1_word1Counts[tag]:
		tau_y1w1[tag][word] = tag1_word1Counts[tag][word]/float(total)




### DECODING
for line in testing:
	i = 2
	lst = ["*STRT*", "*STRT*"] + line.split() + ["*END*", "*END*"]
	length = len(lst)

	sequences = [(["*STRT*", "*STRT*"], 1.0)]

	while i < length:
		word = lst[i]

		possibleTags = [tag  for tag in tau_y1w1 if word in tau_y1w1[tag]] 
		#print len(possibleTags), "poss tags"
		newSeqs = []

		for tag in possibleTags: 

			maxProb = 0.0
			maxSeq = []
			for prevTags_Prob in sequences:

				prevTag = prevTags_Prob[0][-1]
				#print "prev tag ",prevTag

				prevProb = prevTags_Prob[1]
				#print "prev prob ",prevProb

				try:
					newProb = sig_y1y2[prevTag][tag] * tau_y1w1[tag][word] * prevProb
				except KeyError:
					newProb = 0.0

				#print newProb, "for tag ", tag
				if newProb > maxProb: #\geq?
					maxProb = newProb
					maxSeq = list(prevTags_Prob[0]) + list([word])

			maxSeq.append(tag)
			newSeqs.append((maxSeq, maxProb))

		sequences = newSeqs
		#print sequences
		i += 2

	print " ".join(sequences[0][0][2:-2])


