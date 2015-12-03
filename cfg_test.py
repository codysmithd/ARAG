# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 18:11:22 2015

@author: dmc3413
"""

import nltk

groucho_grammar = nltk.CFG.fromstring(
    """
    S -> NP VP
    PP -> P NP
    NP -> Det N | Det N PP | 'I'
    VP -> V NP | VP PP
    Det -> 'an' | 'my'
    N -> 'elephant' | 'pajamas'
    V -> 'shot'
    P -> 'in'
    """
    );
      
print(groucho_grammar)


sent = ['I', 'shot', 'an', 'elephant', 'in', 'my', 'pajamas']


parser = nltk.ChartParser(groucho_grammar)

for tree in parser.parse(sent):
    print(tree)