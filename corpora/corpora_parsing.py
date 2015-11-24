'''
Program to do operations on the corpora
'''
import nltk
from nltk import word_tokenize
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

    #print(pos_tags['NN'])

if __name__ == '__main__':
    get_unique_tags('/computer_science')
