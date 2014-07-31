#!/usr/bin/env python2
from hackergen import phrasegen

def getPhrase(*args, **kwargs):
	return phrasegen.getPhrase(*args, **kwargs)

def printPhrase(*args, **kwargs):
	print getPhrase(*args, **kwargs)

printPhrase()
