import math
import sys

prog_out = open(sys.argv[1], "r").read().split('\n')
correct = open(sys.argv[2], "r").read().split('\n')

precision_num = 0.0
precision_den = 0.0
recall_den = 0.0

for i in range(len(correct)):
    proper_translation = correct[i].split()
    prog_translation = prog_out[i].split()

    if len(prog_translation) <= 10:

	    for eword in prog_translation:
	        if eword in proper_translation:
	            precision_num += 1.0
	        precision_den += 1.0

	    recall_den += sum([1.0 for w in proper_translation])

precision = precision_num/precision_den
recall = precision_num/recall_den

f = 2 * (precision*recall)/(precision + recall)

print f 
