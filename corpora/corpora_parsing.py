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
    pos_tags = set()
    data = ""

    full_path = os.getcwd() + path
    for i in os.listdir(full_path):
        if i.endswith(".txt"):
            with open(full_path + '/' + i, 'r') as f:
                data += f.read().replace('\n', ' ')
    data = ''.join(ch for ch in data if ch not in set(string.punctuation))
    data = nltk.pos_tag(word_tokenize(data))
    for x in data:
        pos_tags.add(x[1])
    print(pos_tags)
    print(len(pos_tags))

if __name__ == '__main__':
    get_unique_tags('/computer_science')
