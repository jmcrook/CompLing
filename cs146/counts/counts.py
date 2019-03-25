import sys

text = open(sys.argv[1], "r").read().split()
words = {}
for t in text:
	if t in words:
		words[t] += 1
	else:
		words[t] = 1

for w in words:
	print w, words[w]

