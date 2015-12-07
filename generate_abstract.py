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
   if word.lower() in dic.keys(): 
       return [len(list(y for y in x if  y[-1].isdigit() ) ) for x in dic[word.lower()]]
   else:
       return []


def applyTrigrams(sentance, trigrams):
    if len(sentance) < 2:
        return []
        
    tagged = nltk.pos_tag(sentance)
    n = 3
    tagged_ngrams = ngrams(tagged, n);

    gram_index = 0
    for tg in tagged_ngrams:
        k = tg[0][1] + " " + tg[1][1] + " " + tg[2][1];
        if k in trigrams[n].keys():
            random.shuffle(trigrams[n][k])
            print("old sent 3")
            print(sentance)
           
            sentance[gram_index] = trigrams[n][k][0][0]
            sentance[gram_index+1] = trigrams[n][k][0][1]
            sentance[gram_index+2] = trigrams[n][k][0][2]
            print("new sent 3")
            print(sentance)
            
        gram_index = gram_index + 1
    return sentance


def applyBigrams(sentance, bigrams):
    if len(sentance) < 2:
        return []
        
    tagged = nltk.pos_tag(sentance)
    n = 3
    tagged_ngrams = ngrams(tagged, n);

    gram_index = 0
    for tg in tagged_ngrams:
        k = tg[0][1] + " " + tg[1][1] + " " + tg[2][1];
        if k in bigrams[n].keys():
            random.shuffle(bigrams[n][k])
            print("old sent 2")
            print(sentance)
           
            sentance[gram_index] = bigrams[n][k][0][0]
            sentance[gram_index+1] = bigrams[n][k][0][1]
            print("new sent 2")
            print(sentance)
            
        gram_index = gram_index + 1
    return sentance



def scoreSentence(s,d):
    '''
    Scores a given genrated sentence based on certain criteria
    '''

    score = 0
    
    syllables = 0
    for word in s:
        syllables += len(nsyl(word,d))
    
    # Flesch reading ease    
    numWords = len(s);
    ease = 206.835 - 1.015*(numWords) - 84.6*(syllables/numWords)
    
    # Duplicate words? Subtract from it's score
    score += len(set(s)) - len(s)

    return score,ease

def outputSentence(s):
    '''
    '''
    output = ''
    if len(s) > 0:
        output += (s[0][0].upper() + s[0][1:])  # make first word capital
        for word in s[1:]:
            output += ' ' + word.lower()
        output += '.'
    return output

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
        s_score, ease = scoreSentence(s,d)
        if s_score > best_score and len(s) > 0:
            best_score = s_score
            best_s = s
            
    
    print(best_s)
    
    print(best_score)
    
    print(ease)


if __name__ == '__main__':
    main()
