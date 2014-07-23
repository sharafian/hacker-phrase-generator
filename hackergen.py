#!/usr/bin/env python2
from random import choice, random
from re import sub

# everything to load the proper words

def toWord(l): 
	if (l[0] == '>'): # start with a '>' for a literal
		return l[1:]
	return ' ' + l.strip()

def ftowl(fname): # file to word list
        return [ toWord(l) for l in open(fname) ]

nounsl = ftowl("nouns.txt")
adjsl = ftowl("adjs.txt")
verbsl = ftowl("verbs.txt")
articlesl = ftowl("articles.txt")
prepsl = ftowl("preps.txt")
conjsl = ftowl("conjs.txt")

def getRandomWord(part):
	return choice({\
"SUBJ"   :nounsl,\
"OBJ"   :nounsl,\
"ADJ"    :adjsl,\
"VERB"   :verbsl,\
"ARTICLE":articlesl,\
"PREP"   :prepsl,\
"CONJ"   :conjsl,
"END"    :[""],\
}[part])

# everything to actually generate the phrases
# hacky, I know, but it uses a boolean to keep track of context
def getNextPart(part, subj):
	l = {
# markov thing to map parts of speech together
		"SUBJ": [ ("VERB",1.0) ],\
		"OBJ": [ ("PREP",0.6), ("CONJ",0.3), ("END",0.1) ],\
		"ADJ": [ ("ADJ",0.3), ("SUBJ",0.7 * (subj)), ("OBJ",0.7 * (not subj)) ],\
		"VERB": [ ("PREP",0.5), ("ARTICLE",0.5) ],\
		"ARTICLE": [ ("ADJ",0.6), ("SUBJ",0.4 * (subj)), ("OBJ",0.4 * (not subj)) ],\
		"PREP": [ ("ARTICLE",1.0) ],\
		"CONJ": [ ("ARTICLE",1.0) ],\
	}[part][:]
	c = random()
	e = None
	while c > 0.0:
		e = l.pop()
		c -= e[1]	

	if (e[0] == "VERB" or e[0] == "CONJ"):
		subj = not subj

	return e[0], subj

def getPhrase():
	part = "ARTICLE"
	phrase = ""
	subj = True # 1 if subject, 2 if object is next
	while True:
		phrase += getRandomWord(part)
		part, subj = getNextPart(part, subj)
		if part == "END":
			# fix 'a' vs 'an'
			return sub(r'\ba ([aeiou])', r'an \1', phrase)[1:] + "."

#print getPhrase()
