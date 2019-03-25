import sys

gold = open(sys.argv[1], "r").read().split('\n')
myOutput = open(sys.argv[2], "r").read().split('\n')

total = 0.0
correct = 0.0

for i in range(len(gold)):
	goldLine = gold[i].split()
	outLine = myOutput[i].split()

	goldTags = [goldLine[d] for d in range(len(goldLine)) if d % 2 == 1]
	outTags = [outLine[d] for d in range(len(outLine)) if d % 2 == 1]

	if (i != 597):
		for t in range(len(goldTags)):
			total += 1.0
			if (goldTags[t] == outTags[t]):
				correct += 1.0

print correct/total
