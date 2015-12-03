"""
This program generates an abstract for a report given a training corpus
Usage: python generate_abstract.py <path_to_corpus>
"""
import argparse
from nltk.parse.generate import generate
from corpora.corpora_parsing import processCorpus
from nltk import word_tokenize

def scoreSentence(s):
    '''
    Scores a given genrated sentence based on certain criteria
    '''

    score = 0

    # Duplicate words? Subtract from it's score
    score += len(set(s)) - len(s)

    return score

def main():

    # Config
    MAX_NUM_SENTENCES = 1000

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
    for s in generate(cfg_grammer, depth=3, n=MAX_NUM_SENTENCES):
        s_score = scoreSentence(s)
        if s_score > best_score and len(s) > 0:
            best_score = s_score
            best_s = s
    print(best_s)
    #print(best_score)

if __name__ == '__main__':
    main()
