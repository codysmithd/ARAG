'''
Program to do operations on the corpora
'''
import nltk
from nltk import word_tokenize
from nltk.util import ngrams
import re
import os
import string

def get_unique_tags(path):
    '''
    Gets the unique set of POS tags from the specified corpus
    '''
    pos_tags = {}
    data = ""

    # Get all text from selected path
    full_path = os.getcwd() + path
    for i in os.listdir(full_path):
        if i.endswith(".txt"):
            with open(full_path + '/' + i, 'r') as f:
                data += f.read().replace('\n', ' ')

    # Cut out punctuation and tag tokenized words with tags from Penn Treebank
    data = ''.join(ch for ch in data if ch not in set(string.punctuation))
    data = nltk.pos_tag(word_tokenize(data))

    for x in data:
        pos_tags[x[1]] = pos_tags.get(x[1], set())
        pos_tags[x[1]].add(x[0])

    data = sorted(pos_tags, key=pos_tags.get, reverse=True)
    for pos in data:
        print(pos + ": " + str(len(pos_tags[pos])))

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

def get_ngrams(path,n):
    '''
    Gets a set of ngrams from a path
    '''
    data = ""

    # Get all text from selected path
    full_path = os.getcwd() + path
    for i in os.listdir(full_path):
        if i.endswith(".txt"):
            with open(full_path + '/' + i, 'r') as f:
                data += f.read().replace('\n', ' ')

    # Separt lists for sentences
    sentences = [[]]
    addedWord = []
    idx = 0;
    for word in data.split():
        if "." not in word:
            word = re.sub("[,-\/#'!?\"$%|<>\^&\*\]\[;:\+{}=\-_`~()]","",word)
            sentences[idx].append(word)
            addedWord.append(word);
        elif re.search('[0-9].[0-9]',word) != None:
            sentences[idx].append(word)
            addedWord.append(word);
        else:
            word = re.sub("[,-\/#'!?\"$%|<>\^&\*\]\[;:\+{}=\-_`~()]","",word)
            word = word.replace('.','');
            sentences[idx].append(word)
            addedWord.append(word);
            sentences.append([]);
            idx = idx + 1;

    grams = [];
    for sent in sentences:
        tup = ngrams(sent, n);
        for g in tup:
            grams.append(g)


    return set(grams);


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
            with open(full_path + '/' + i, 'r',encoding="utf8") as f:
                data += f.read().replace('\n', ' ')

    if verbose: print('Corpus extracted. Processing.')

    # Strip out chars we don't like
    whitelist = ['.', ' ', '-', '*'] + [c for c in (string.ascii_letters + string.digits)]
    s = ''
    for c in data:
        if c in whitelist:
            s += c
    data = s

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
    grams = {};
    bigrams = {};
    trigrams = {};
    # Loop over each sentence and add sentence_rules, grams, and vocab
    for s in sentences:

        # Cut out punctuation and tag tokenized words with tags from Penn Treebank
        tagged = nltk.pos_tag(s)

        # If we have a non-empty sentence
        if len(tagged):

            sentence_rule = []
            tagged_bigrams = ngrams(tagged, 2);
            tagged_trigrams = ngrams(tagged, 3);


            for tg in tagged_bigrams:
                k = tg[0][1] + " " + tg[1][1]
                if k not in bigrams.keys():
                    bigrams[k] = []
                bigrams[k].append((tg[0][0],tg[1][0]))

            for tg in tagged_trigrams:
                k = tg[0][1] + " " + tg[1][1] + " " + tg[2][1];
                if k not in trigrams.keys():
                    trigrams[k] = []
                trigrams[k].append((tg[0][0],tg[1][0],tg[2][0]))

            # For each tagged word (word, pos)
            for tup in tagged:
                if tup[1] != '-NONE-':
                    sentence_rule.append(tup[1])
                    vocab_dict[tup[1]] = vocab_dict.get(tup[1],set())
                    vocab_dict[tup[1]].add(tup[0])

            sentence_rules.append(sentence_rule)

    # String used to create grammar
    all_grammar = ''

    # Add sentence rule to grammar
    for rule in sentence_rules:
        if score_sentence_rule(rule) >= min_sent_rule_score:
            rule_text = ''
            for pos in rule:
                rule_text += pos + ' '
            all_grammar += '\nS -> {0}'.format(rule_text)

    # Add vocab by POS
    for tag in vocab_dict:

        # Make string of vocab words: word1 | word2 | word3
        vocab_list = ''
        vocab_set = vocab_dict[tag]
        if len(vocab_set):
            last_word = vocab_set.pop()
            for word in vocab_set:
                vocab_list += " '{0}' |".format(word)
            vocab_list += last_word

        all_grammar += '\n{0} -> {1}'.format(tag, vocab_list)

    # Get rid of $, in lue of S
    all_grammar = all_grammar.replace('$', 'S')

    if verbose:
        print('Processing done. Made grammar:')
        #print(all_grammar)

    return bigrams, trigrams, nltk.CFG.fromstring(all_grammar)
