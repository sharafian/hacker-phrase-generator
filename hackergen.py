#!/usr/bin/env python2
from random import choice, random
from re import sub

# everything to load the proper words
def ftowl(fname): # file to word list
        return [ l.strip() for l in open(fname) ]
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
def getNextPart(part):
	l = {
# markov thing to map parts of speech together
		"SUBJ": [ ("VERB",0.7), ("CONJ",0.3) ],\
		"OBJ": [ ("PREP",0.6), ("CONJ",0.3), ("END",0.1) ],\
		"ADJ": [ ("ADJ",0.2), ("SUBJ",0.4), ("OBJ",0.4) ],\
		"VERB": [ ("PREP",0.5), ("ARTICLE",0.5) ],\
		"ARTICLE": [ ("ADJ",0.6), ("SUBJ",0.2), ("OBJ",0.2) ],\
		"PREP": [ ("ARTICLE",1.0) ],\
		"CONJ": [ ("ARTICLE",0.6), ("PREP",0.4) ],\
	}[part][:]
	c = random()
	e = None
	while c > 0.0:
		e = l.pop()
		c -= e[1]	
	return e[0]

def getPhrase():
	part = "ARTICLE"
	phrase = ""
	while True:
		phrase += getRandomWord(part) + " "
		part = getNextPart(part)
		if part == "END":
			return sub(r'a ([aeiou])', r'an \1', phrase)[:-1] + "."

#print getPhrase()
