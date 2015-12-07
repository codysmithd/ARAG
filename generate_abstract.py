"""
This program generates an abstract for a report given a training corpus
Usage: python generate_abstract.py <path_to_corpus>
"""
import argparse
import nltk
from nltk.parse.generate import generate
from corpora.corpora_parsing import processCorpus
from nltk import word_tokenize
from nltk.util import ngrams
import random
import string

#from curses.ascii import isdigit
from nltk.corpus import cmudict

def nsyl(word,dic):
   if word.lower() in dic.keys():
       return [len(list(y for y in x if  y[-1].isdigit() ) ) for x in dic[word.lower()]]
   else:
       return []

def applyBigrams(sentence, bigrams):
    if len(sentence) < 2:
        return []

    tagged = nltk.pos_tag(sentence)
    tagged_ngrams = ngrams(tagged, 2);

    gram_index = 0
    for tg in tagged_ngrams:
        k = tg[0][1] + " " + tg[1][1] + " " + tg[2][1];
        if k in bigrams.keys():
            random.shuffle(bigrams[k])
            sentence[gram_index] = bigrams[k][0][0]
            sentence[gram_index+1] = bigrams[k][0][1]


        gram_index = gram_index + 1
    return sentence


def applyTrigrams(sentence, trigrams):
    if len(sentence) < 3:
        return []

    tagged = nltk.pos_tag(sentence)
    tagged_ngrams = ngrams(tagged, 3);

    gram_index = 0
    for tg in tagged_ngrams:
        k = tg[0][1] + " " + tg[1][1] + " " + tg[2][1];
        if k in trigrams.keys():
            random.shuffle(trigrams[k])

            sentence[gram_index] = trigrams[k][0][0]
            sentence[gram_index+1] = trigrams[k][0][1]
            sentence[gram_index+2] = trigrams[k][0][2]

        gram_index = gram_index + 1
    return sentence



def applyPOSBigrams(taggedSentence, bigrams):
    if len(taggedSentence) < 2:
        return []

    tagged_ngrams = ngrams(taggedSentence, 2);

    sentence = ['']*len(taggedSentence)

    gram_index = 0
    for tg in tagged_ngrams:
        k = tg[0] + " " + tg[1];
        if k in bigrams.keys():
            if len(bigrams[k]) > 1:
                random.shuffle(bigrams[k])
                sentence[gram_index] = bigrams[k][0][0]
                sentence[gram_index+1] = bigrams[k][0][1]
    

        gram_index = gram_index + 1
    return sentence



def applyPOSTrigrams(taggedSentence, trigrams):
    if len(taggedSentence) < 3:
        return []


    tagged_ngrams = ngrams(taggedSentence, 3);

    sentence = ['']*len(taggedSentence)
    
    gram_index = 0
    for tg in tagged_ngrams:
        k = tg[0]+ " " + tg[1] + " " + tg[2];
        
        if k in trigrams.keys():
            if len(trigrams[k]) > 1:
                random.shuffle(trigrams[k])
    
                sentence[gram_index] = trigrams[k][0][0]
                sentence[gram_index+1] = trigrams[k][0][1]
                sentence[gram_index+2] = trigrams[k][0][2]

        gram_index = gram_index + 1
    return sentence




def scoreSentence(s,d):
    '''
    Scores a given genrated sentence based on certain criteria
    '''

    score = 0

    # Duplicate words? Subtract from it's score
    score += len(set(s)) - len(s)

    length = len(s)
    
    syllables = 0
    for word in s:
        syllables += len(nsyl(word,d))

    # Flesch reading ease
    numWords = len(s);
    f_ease = 206.835 - 1.015*(numWords) - 84.6*(syllables/numWords)
    # 90.0–100.0	easily understood by an average 11-year-old student
    # 60.0–70.0	easily understood by 13- to 15-year-old students
    # 0.0–30.0	best understood by university graduates

    # Flesch–Kincaid grade level
    f_grade = 0.39*(numWords) + 11.8*(syllables/numWords) - 15.59

    return f_ease,f_grade,length

def outputSentence(s):
    '''
    '''
    output = ''
    if s[0] == '':
        s = s[1:]
    
    if len(s) > 0:
        
        if s[0][0] in string.ascii_letters:
            output += (s[0][0].upper() + s[0][1:])  # make first word capital
        for word in s[1:]:
            output += ' ' + word.lower()
        output += '.'
    return output

def main():


    # Argument Parsing
    parser = argparse.ArgumentParser(description="""
        Generates a report abstract given a path to a corpus of abstracts
    """)
    parser.add_argument('path_to_corpus', help='Path to corpus of abstacts')
    args = parser.parse_args()

    # Find the corpus and get the ngrams dictionary and cfg grammer from it
#    bigrams, trigrams, cfg_grammer = processCorpus(args.path_to_corpus, verbose=True)
    bigrams, trigrams, rules = processCorpus(args.path_to_corpus, verbose=True)

    print('Grammer done. Making sentences.')

    # Print out max sentences generated from the cfg
    best_score = float('-inf')
    best_s = ''
    best_ease = 0
    best_grade = 0
    n_sent = 0
    
    d = cmudict.dict() 

    rule_size_array = []
    for rule in rules:    
        rule_size_array.append(len(rule))
    
    rule_size_array = sorted(rule_size_array)
    mean_sent_size = sum(rule_size_array)/len(rule_size_array)


#    for s in generate(cfg_grammer, depth=3, n=MAX_NUM_SENTENCES):
    for rule in rules:
        s = applyPOSBigrams(rule,bigrams);
        s = applyPOSTrigrams(rule,trigrams);
       
        fease, fgrade, length = scoreSentence(s,d)
        
        ss = 0-abs(length - mean_sent_size)
#        ss =  100
        n_sent = n_sent + 1
        if ss > best_score and len(s) > 0:
            best_score = ss
            best_s = s
            best_ease = fease
            best_grade = fgrade
        
        

    print(outputSentence(best_s))
    print(best_score)
    print(best_ease)
    print(best_grade)
    print(n_sent)


if __name__ == '__main__':
    main()
