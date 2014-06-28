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

def getRandomWord(part):
	return choice({\
"NOUN"   :nounsl,\
"ADJ"    :adjsl,\
"VERB"   :verbsl,\
"ARTICLE":articlesl,\
"PREP"   :prepsl,\
"END"    :[""],\
}[part])

# everything to actually generate the phrases
def getNextPart(part):
	l = {
# markov thing to map parts of speech together
		"NOUN": [ ("VERB",0.5), ("PREP",0.4), ("END",0.1) ],\
		"ADJ": [ ("ADJ",0.2), ("NOUN",0.8) ],\
		"VERB": [ ("PREP",0.5), ("ARTICLE",0.5) ],\
		"ARTICLE": [ ("ADJ",0.7), ("NOUN",0.3) ],\
		"PREP": [ ("ARTICLE",1.0) ],\
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

print getPhrase()
