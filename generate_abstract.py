"""
This program generates an abstract for a report given a training corpus
Usage: python generate_abstract.py <path_to_corpus>
"""
import argparse
from corpora.corpora_parsing import processCorpus

def main():

    # Argument Parsing
    parser = argparse.ArgumentParser(description="""
        Generates a report abstract given a path to a corpus of abstracts
    """)
    parser.add_argument('path_to_corpus', help='Path to corpus of abstacts')
    args = parser.parse_args()

    # Find the corpus and get the ngrams dictionary and cfg grammer from it
    ngrams, cfg_object = processCorpus(args.path_to_corpus)

    # Print out sentences generated from the cfg
    #TODO

if __name__ == '__main__':
    main()
