"""
This program generates an abstract for a report given a training corpus
Usage: python generate_abstract.py <path_to_corpus>
"""
import argparse
import nltk
from nltk.parse.generate import generate
from corpora.corpora_parsing import processCorpus
from nltk import word_tokenize
#from curses.ascii import isdigit 
from nltk.corpus import cmudict 

def nsyl(word,dic): 
   return [len(list(y for y in x if  y[-1].isdigit() ) ) for x in dic[word.lower()]] 

def scoreSentence(s,d):
    '''
    Scores a given genrated sentence based on certain criteria
    '''

    score = 0
    
    syllables = 0
    for word in s:
        syllables += len(nsyl(word,d))

    # Duplicate words? Subtract from it's score
    score += len(set(s)) - len(s)

    return score,syllables

def main():

    # Config
    MAX_NUM_SENTENCES = 100

    # Argument Parsing
    parser = argparse.ArgumentParser(description="""
        Generates a report abstract given a path to a corpus of abstracts
    """)
    parser.add_argument('path_to_corpus', help='Path to corpus of abstacts')
    args = parser.parse_args()

    # Find the corpus and get the ngrams dictionary and cfg grammer from it
    ngrams, cfg_grammer = processCorpus(args.path_to_corpus, verbose=True)

    print('Grammer done. Making sentences.')

    # Print out max sentences generated from the cfg
    best_score = float('-inf')
    best_s = ''
    
    d = cmudict.dict() 

    for s in generate(cfg_grammer, depth=3, n=MAX_NUM_SENTENCES):
        s_score, syllables = scoreSentence(s,d)
        if s_score > best_score and len(s) > 0:
            best_score = s_score
            best_s = s
            
    
    print(best_s)
    print(best_score)
    print(syllables)
    
if __name__ == '__main__':
    main()
