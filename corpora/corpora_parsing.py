'''
Program to do operations on the corpora
'''
import nltk
from nltk import word_tokenize
from nltk.util import ngrams
import re
import os
import string


tag_set = None

def score_sentence_rule(pos_list):
    '''
    Given a list of POS tags for sentence, returns a score
    '''
    score = 0

    # Subtract if there are the same tag next to each other
    for i in range(1,len(pos_list)):
        if pos_list[i] == pos_list[i-1]:
            score -= 10

    # Add if sentence is all unique items
    if len(set(pos_list)) == len(pos_list):
        score += 1

    if len(pos_list) > 14:
        score -= 10

    return score


def processCorpus(path, verbose=False, min_sent_rule_score=0):
    '''
    Processes a corpus. Returns a dictionary of ngrams, and a CFG
    Params:
        path: string path to the corpus (e.g. /corpora/nanocomputing)
        [verbose]: verbose mode on or off
        [min_sent_rule_score]: the min value a sentence can have to get added
    '''

    data = ""

    # Get all text from selected path
    full_path = os.getcwd() + path
    for i in os.listdir(full_path):
        if i.endswith(".txt"):
            print('Reading ' +i)
            with open(full_path + '/' + i, 'r',encoding="utf8") as f:
                data += f.read()

    # Strip out unwanted characters
    data.replace('\n', ' ')

    # Chacters we want to remove
    blacklist = ['(', ')', ',', '"']

    # Pre-processing
    processed_data = ''
    for c in data:

        # Get rid of duplicate spaces
        if c == ' ' and processed_data[-1] != ' ':
            processed_data += c

        # Get rid of characters in blacklist
        elif c not in blacklist:
            processed_data += c

    data = processed_data

    # Make a 2D array of sentences
    sentences = [[]]
    idx = 0;
    for word in data.split():
        if '.' not in word:
            sentences[idx].append(word)
        elif re.search('[0-9].[0-9]',word) != None:
            sentences[idx].append(word)
        else:
            sentences[idx].append(word.replace('.', ''))
            sentences.append([]);
            idx = idx + 1;

    vocab_dict = {}
    sentence_rules = []

    # Dictionary where keys are n -> which is dictionary of keys that are POS + POS + ...
    _ngrams = {}
    for n in range(1, 5):
        _ngrams[n] = {}

    if verbose: print('Corpus extracted. Processing.')

    # Loop over each sentence and add sentence_rules, grams, and vocab
    for s in sentences:

        # Cut out punctuation and tag tokenized words with tags from Penn Treebank
        tagged = nltk.pos_tag(s, tagset=tag_set)
        
        # If we have a non-empty sentence
        if len(tagged):

            # Make ngrams for n in range
            for n in range(1,5):
                for g in ngrams(tagged, n):

                    # Make key for POS ngram
                    key = str(g[0][1])
                    for x in range(1, len(g)):
                        key += ' ' + g[x][1]

                    # Add tuple of words to dictionary at key
                    if key not in _ngrams[n].keys(): _ngrams[n][key] = []
                    _ngrams[n][key].append( tuple([g[i][0] for i in range(0,n)]) )

            # Make sentence rule
            sentence_rule = []
            shouldAddSentenceRule = True

            for tup in tagged:
                word, tag = tup[0], tup[1]

                # If we have duplicate tags next to each other or something we couldn't tag, lets not add it
                if tag == '-NONE-' or (len(sentence_rule) and tag == sentence_rule[-1]):
                    shouldAddSentenceRule = False
                    break
                else:
                    # Add it to the sentence rule and add the word to vocab
                    sentence_rule.append(tag)
                    vocab_dict[tag] = vocab_dict.get(tag,set())
                    vocab_dict[tag].add(word)

            if shouldAddSentenceRule:
                sentence_rules.append(sentence_rule)

    return _ngrams, sentence_rules
