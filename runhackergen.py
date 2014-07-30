#!/usr/bin/env python2
from hackergen import phrasegen

def getPhrase(*args, **kwargs):
	return phrasegen.getPhrase(*args, **kwargs)

def printPhrase(*args, **kwargs):
	print "Generated Phrase:\n\n"+getPhrase(*args, **kwargs)

printPhrase()
