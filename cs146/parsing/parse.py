import sys
import time
import math

rules = open(sys.argv[1], "r").read().split("\n")
sentences = [s.split() for s in open(sys.argv[2], "r").read().split("\n")]

binaryCounts = {}
unaryCounts = {}

binaryTotals = {}
unaryTotals = {}

non_terminals = {}
labelToUnary1 = {}

labelToBinary1 = {}
leftUpRight1 = {}

## Counting Rules
for r in rules: # 5 NP --> DT_NNPS NN
	splitRule = r.split()
	if splitRule != []:
		count = float(splitRule[0])
		lhs = splitRule[1] # left hand side
		rhs = tuple(splitRule[3:8]) # right hand side

		if lhs not in non_terminals:
			non_terminals[lhs] = 0
			labelToBinary1[lhs] = []

	    # check if unary or binary rule
		if len(rhs) == 2:
	    	# checks if this lhs has not been encountered before
			if lhs not in binaryCounts:
				binaryCounts[lhs] = {}
				binaryTotals[lhs] = count
			else:
				binaryTotals[lhs] += count

			binaryCounts[lhs][rhs] = count

			if rhs[0] not in leftUpRight1:
				leftUpRight1[rhs[0]] = {}

			if lhs not in leftUpRight1[rhs[0]]:
				leftUpRight1[rhs[0]][lhs] = {}

			leftUpRight1[rhs[0]][lhs][rhs[1]] = 0


		else: #if count > 1:
			# checks if this lhs has not been encountered before
			if lhs not in unaryCounts:
				unaryCounts[lhs] = {}
				unaryTotals[lhs] = count
			else:
				unaryTotals[lhs] += count

			unaryCounts[lhs][rhs] = count

			if rhs[0] not in labelToUnary1:
				labelToUnary1[rhs[0]] = []

			if lhs not in labelToUnary1[rhs[0]]:
				labelToUnary1[rhs[0]].append(lhs)


## Getting Probs

ruleProbs1 = {}

for lhs in non_terminals:
	ruleProbs1[lhs] = {}

	if lhs in unaryTotals:
		unaryTotal = unaryTotals[lhs]

		##unary rules takes strings as keys, not tuples
		for rhs in unaryCounts[lhs]:
			ruleProbs1[lhs][rhs[0]] = -math.log(unaryCounts[lhs][rhs]/unaryTotal)

	if lhs in binaryTotals:
		binaryTotal = binaryTotals[lhs]

		for rhs in binaryCounts[lhs]:
			ruleProbs1[lhs][rhs] = -math.log(binaryCounts[lhs][rhs]/binaryTotal)


def fill(sentence, chart, i, k, ruleProbs, labelToUnary, leftUpRight):
	#print k- i
	#STEP 1
	if k == i + 1:
		chart[i][k][sentence[i]] = {0: sentence[i], 1: None, 2: None, 3: 0.0}

	# step 2, 
	for j in range(i + 1, k):

		for llabel in chart[i][j]:
			leftConstituent =  chart[i][j][llabel]

			if leftConstituent[0] in leftUpRight:

				for newLabel in leftUpRight[leftConstituent[0]]:

					for rlabel in leftUpRight[leftConstituent[0]][newLabel]:


						if rlabel in chart[j][k]:
							rightConstituent =  chart[j][k][rlabel]


							mu = leftConstituent[3] + rightConstituent[3] + ruleProbs[newLabel][(leftConstituent[0],rightConstituent[0])]

							if (newLabel not in chart[i][k]) or (chart[i][k][newLabel][3] > mu):
								chart[i][k][newLabel] =  {0: newLabel, 1: leftConstituent, 2: rightConstituent, 3: mu}

	## step 3, 
	notDone = True
	oldConstituents = dict(chart[i][k])
	while notDone:
		notDone = False
		for rlabel in chart[i][k]:
			newConstituents = {}
			if rlabel != "TOP" and rlabel in labelToUnary:
				constituent = chart[i][k][rlabel] #oldConstituents[rlabel]
				for newLabel in labelToUnary[rlabel]:
					mu = ruleProbs[newLabel][rlabel] + constituent[3]
					if newLabel in oldConstituents: 
						if oldConstituents[newLabel][3] > mu:
							newConstituents[newLabel] = {0:newLabel, 1: constituent,2 : None, 3: mu}
							notDone = True
					else:
						newConstituents[newLabel] = {0:newLabel, 1: constituent, 2: None, 3: mu}	
						notDone = True
			oldConstituents.update(newConstituents)
		chart[i][k] = dict(oldConstituents)


def clean(tree):
	if tree != None:
		if tree[1] == None:
			sys.stdout.write(tree[0])
		else:
			sys.stdout.write("(" + tree[0] + " ")
			clean(tree[1])
			clean(tree[2])
			sys.stdout.write(")")



def parse(sent, maxlen):
	L = len(sent)
	if L <= maxlen:

		chart = {z: {x: {} for x in range(L+1)} for z in range(L+1)}

		for l in range (1, L+1):
			for s in range(0, (L-l+1)):
				fill(sent, chart, s, s+l, ruleProbs1, labelToUnary1, leftUpRight1)

		clean(chart[0][L]["TOP"])
		sys.stdout.write("\n")
	else:
		sys.stdout.write("*IGNORE*\n")

for s in sentences:
	parse(s, 25)