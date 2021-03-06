#!/usr/bin/env python2
from random import choice, random
from re import sub
import os.path

# everything to load the proper words

def toWord(l): 
	if (l[0] == '>'): # start with a '>' for a (mostly) literal
		return l.strip()[1:]
	return ' ' + l.strip()

dirprefix = "hackergen"
def ftowl(fname): # file to word list
	return [ toWord(l) for l in open(os.path.join(dirprefix, fname), "rb") ]

nounsl = ftowl("nouns.txt")
adjsl = ftowl("adjs.txt")
verbsl = ftowl("verbs.txt")
articlesl = ftowl("articles.txt")
prepsl = ftowl("preps.txt")
conjsl = ftowl("conjs.txt")

original_verbsl = verbsl[:]

def toACT(verb):
	if verb.endswith("s") or verb.endswith("y"):
		return (verb+"es")
	else:
		return (verb+"s")
def toFUT(verb):
	return (" will"+verb)
def toINF(verb):
	if verb.endswith("e"):
		return (verb[:-1]+"ing")
	elif verb.endswith("p"):
		return (verb+"ping")
	else:
		return (verb+"ing")
def toPAS(verb):
	if verb == "run":
		verbsl.append("ran")
	elif verb.endswith("e"):
		verbsl.append(verb+"d")
	elif verb.endswith("p"):
		verbsl.append(verb+"ped")
	else:
		verbsl.append(verb+"ed")
tenses = {
	"ACT" : toACT,
	"FUT" : toFUT,
	"INF" : toINF,
	"PAS" : toPAS,
}

def tense(choice="FUT"):
	"""Converts The Verbs To A Specific Tense."""
	global verbsl

	choice = choice.upper()		# Allow tense names to be in lowercase
	if choice in tenses:		# Remember, Python throws an error if you try and get a key that doesn't exist, so we need to do this
		vtt = tenses[choice]
	else:							
		raise ValueError("Unrecognized tense "+str(choice))

	verbsl[:] = [ vtt(v) for v in verbsl ]
	
tense()

def getRandomWord(part):
	return choice({
		"SUBJ"   :nounsl,
		"OBJ"   :nounsl,
		"ADJ"    :adjsl,
		"VERB"   :verbsl,
		"ARTICLE":articlesl,
		"PREP"   :prepsl,
		"CONJ"   :conjsl,
		"END"    :[""],
		}[part])

# everything to actually generate the phrases
# hacky, I know, but it uses a boolean to keep track of context
def getNextPart(part, subj):
	l = {
# markov thing to map parts of speech together
		"SUBJ": [ ("VERB",1.0) ],
		"OBJ": [ ("PREP",0.6), ("CONJ",0.3), ("END",0.1) ],
		"ADJ": [ ("ADJ",0.3), ("SUBJ",0.7 * (subj)), ("OBJ",0.7 * (not subj)) ],
		"VERB": [ ("PREP",0.5), ("ARTICLE",0.5) ],
		"ARTICLE": [ ("ADJ",0.6), ("SUBJ",0.4 * (subj)), ("OBJ",0.4 * (not subj)) ],
		"PREP": [ ("ARTICLE",1.0) ],
		"CONJ": [ ("ARTICLE",1.0) ],
	}[part][:]
	c = random()
	e = None
	while c > 0.0:
		e = l.pop()
		c -= e[1]	

	if (e[0] == "VERB" or e[0] == "CONJ"):
		subj = not subj

	return e[0], subj

def formatPhrase(phrase):
	return sub(r'\ba ([aeiou])', r'an \1', phrase)[1:] + "."

def getPhrase(limit = -1):
	part = "ARTICLE"
	phrase = ""
	ccount = 0 # counts conjunctions
	subj = True # 1 if subject, 2 if object is next
	while True:

		if part == "CONJ":
			ccount += 1
			if ccount == limit:
				return formatPhrase(phrase)

		phrase += getRandomWord(part)
		part, subj = getNextPart(part, subj)
		if part == "END":
			# fix 'a' vs 'an'
			return formatPhrase(phrase)

#print getPhrase()
