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

#tag_set = 'universal'
tag_set = None

def nsyl(word,dic):
   if word.lower() in dic.keys():
       return [len(list(y for y in x if  y[-1].isdigit() ) ) for x in dic[word.lower()]]
   else:
       return []


def applyBigrams(sentence, bigrams):
    if len(sentence) < 2:
        return []

    tagged = nltk.pos_tag(sentence, tagset=tag_set)
    tagged_ngrams = ngrams(tagged, 2);

    gram_index = 0
    for tg in tagged_ngrams:
        k = tg[0][1] + " " + tg[1][1]
        if k in bigrams.keys():
            if len(bigrams[k]) > 1:
                random.shuffle(bigrams[k])

                sentence[gram_index] = bigrams[k][0][0]
                sentence[gram_index+1] = bigrams[k][0][1]


        gram_index = gram_index + 1
    return sentence


def applyTrigrams(sentence, trigrams):
    if len(sentence) < 3:
        return []
    
    tagged = nltk.pos_tag(sentence, tagset=tag_set)
    tagged_ngrams = ngrams(tagged, 3);

    gram_index = 0
    for tg in tagged_ngrams:
        k = tg[0][1] + " " + tg[1][1] + " " + tg[2][1];
        if k in trigrams.keys():
            if len(trigrams[k]) > 1:
                random.shuffle(trigrams[k])

                sentence[gram_index] = trigrams[k][0][0]
                sentence[gram_index+1] = trigrams[k][0][1]
                sentence[gram_index+2] = trigrams[k][0][2]

        gram_index = gram_index + 1
    return sentence


def applyQuadgrams(sentence, quadgrams):
    if len(sentence) < 3:
        return []

    tagged = nltk.pos_tag(sentence, tagset=tag_set)
    tagged_ngrams = ngrams(tagged, 4);

    gram_index = 0
    for tg in tagged_ngrams:
        k = tg[0][1] + " " + tg[1][1] + " " + tg[2][1] + " " + tg[3][1];
        if k in quadgrams.keys():
            if len(quadgrams[k]) > 1:
                random.shuffle(quadgrams[k])

                sentence[gram_index] = quadgrams[k][0][0]
                sentence[gram_index+1] = quadgrams[k][0][1]
                sentence[gram_index+2] = quadgrams[k][0][2]
                sentence[gram_index+2] = quadgrams[k][0][3]
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
            if len(bigrams[k]) > 0:
                random.shuffle(bigrams[k])

                skip = False
                for word in bigrams[k][0]:
                    if word == '':
                        skip = True
                    

                if not skip:
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
                skip = False
                for word in trigrams[k][0]:
                    if word == '':
                        skip = True

                if not skip:
                    sentence[gram_index] = trigrams[k][0][0]
                    sentence[gram_index+1] = trigrams[k][0][1]
                    sentence[gram_index+2] = trigrams[k][0][2]

        gram_index = gram_index + 1
    return sentence

def applyPOSQuadgrams(taggedSentence, quadgrams):
    if len(taggedSentence) < 4:
        return []


    tagged_ngrams = ngrams(taggedSentence, 4);
    sentence = ['']*len(taggedSentence)

    gram_index = 0
    for tg in tagged_ngrams:
        k = tg[0]+ " " + tg[1] + " " + tg[2]  + " " + tg[3]

        if k in quadgrams.keys():
            if len(quadgrams[k]) > 1:
                random.shuffle(quadgrams[k])

                skip = False
                for word in quadgrams[k][0]:
                    if word == '':
                        skip = True

                if not skip:
                    sentence[gram_index] = quadgrams[k][0][0]
                    sentence[gram_index+1] = quadgrams[k][0][1]
                    sentence[gram_index+2] = quadgrams[k][0][2]
                    sentence[gram_index+3] = quadgrams[k][0][3]

        gram_index = gram_index + 1
    return sentence





def applyBigramsSubjectMatch(sentence, bigrams, subject):
    if len(sentence) < 2:
        return []
    
    tagged = nltk.pos_tag(sentence, tagset=tag_set)
    tagged_ngrams = ngrams(tagged, 2);

    gram_index = 0
    for tg in tagged_ngrams:
        k = tg[0][1] + " " + tg[1][1];
        if 'NNP' in k.split():
            if k in bigrams.keys():
                random.shuffle(bigrams[k])
                if tg[0][1] == 'NNP':
                    sentence[gram_index] = subject[0].split()[0]
                    sentence[gram_index+1] = bigrams[k][0][1]
                elif tg[1][1] == 'NNP':
                    sentence[gram_index] = bigrams[k][0][0]
                    sentence[gram_index+1] = subject[0].split()[0]

        gram_index = gram_index + 1
    return sentence
    
def applyTrigramsSubjectMatch(sentence, trigrams, subject):
    if len(sentence) < 3:
        return []
    
    tagged = nltk.pos_tag(sentence, tagset=tag_set)
    tagged_ngrams = ngrams(tagged, 3);

    gram_index = 0
    for tg in tagged_ngrams:
        k = tg[0][1] + " " + tg[1][1] + " " + tg[2][1];
        if 'NNP' in k.split():
            if k in trigrams.keys():
                random.shuffle(trigrams[k])
                if tg[0][1] == 'NNP':
                    sentence[gram_index] = subject[0].split()[0]
                    sentence[gram_index+1] = trigrams[k][0][1]
                    sentence[gram_index+2] = trigrams[k][0][2]
                elif tg[1][1] == 'NNP':
                    sentence[gram_index] = trigrams[k][0][0]
                    sentence[gram_index+1] = subject[0].split()[0]
                    sentence[gram_index+2] = trigrams[k][0][2]
                elif tg[2][1] == 'NNP':
                    sentence[gram_index] = trigrams[k][0][0]
                    sentence[gram_index+1] = trigrams[k][0][1]
                    sentence[gram_index+2] = subject[0].split()[0]

        gram_index = gram_index + 1
    return sentence
    
def scoreSentence(s,d):
    '''
    Scores a given genrated sentence based on certain criteria
    '''

    score = 0

    # Duplicate words? Subtract from it's score
    score += (len(set(s)) - len(s)) * 10

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


def outputSentence(s,subject):
    '''
    '''

    output = ''

    if len(s) > 0:
        if s[0][0] in string.ascii_letters:
            output += (s[0][0].upper() + s[0][1:])  # make first word capital
        for word in s[1:]:
            if word == subject:
                output += ' ' + word
            elif word in ['a','I']:
                output += ' ' + word
            else:
                output += ' ' + word.lower()
        output += '.'
    return output



def scoreRule_A(rule,freq_dist_rules_list,mean_sent_size):
    total = 0;
    top_ten = []
    i = 0
    for r in freq_dist_rules_list:
        total += r[1]
        if i < 10:
            top_ten.append(r[0])
            i+=1
    
    result = 0;
    for tag in rule:
        if tag == 'NNP':
            result += 5
        if tag in top_ten:
            result += 1;

    
    result = result - abs(len(rule) - mean_sent_size)    
    
    return result
    
def main():


    # Argument Parsing
    parser = argparse.ArgumentParser(description="""
        Generates a report abstract given a path to a corpus of abstracts
    """)
    parser.add_argument('path_to_corpus', help='Path to corpus of abstacts')
    args = parser.parse_args()

    # Find the corpus and get the ngrams dictionary and cfg grammer from it
#    bigrams, trigrams, cfg_grammer = processCorpus(args.path_to_corpus, verbose=True)
    #bigrams, trigrams, rules = processCorpus(args.path_to_corpus, verbose=True)
    ngrams, rules = processCorpus(args.path_to_corpus, verbose=True)
    bigrams = ngrams[2]
    trigrams = ngrams[3]
    quadgrams = ngrams[4]

#    print(bigrams)
#
    print('Grammer done. Making sentences.')

    # Print out max sentences generated from the cfg
    common_nouns = {}
    for k in bigrams:
        for tup in bigrams[k]:
            pos_one =  k.split()[0][0];
            pos_two =  k.split()[1][0];
            if pos_one == 'N':
                key = tup[0] + " " + k.split()[0];

                if key not in common_nouns.keys():
                    common_nouns[key] = 0
                common_nouns[key]+=1
                
            if pos_two == 'N':
                key = tup[1] + " " + k.split()[1];
                if key not in common_nouns.keys():
                    common_nouns[key] = 0
                common_nouns[key]+=1
    common_nouns_list = []
    for k in common_nouns:
        common_nouns_list.append((k,common_nouns[k]))
    common_nouns_list.sort(key=lambda tup: tup[1]) 
    common_nouns_list_nnp = []
    
    for t in common_nouns_list:
        if t[0].split()[1] == 'NNP':
            common_nouns_list_nnp.append(t)
#            print(t)
    
    d = cmudict.dict()

    rule_size_array = []
    for rule in rules:
        rule_size_array.append(len(rule))

    rule_size_array = sorted(rule_size_array)
    mean_sent_size = sum(rule_size_array)/len(rule_size_array)

    best_sentences = []
    best_rules = []
   
    freq_dist_rules = {}
    for rule in rules:
        for tag in rule:
            if tag not in freq_dist_rules:
                freq_dist_rules[tag] = 0
                
            freq_dist_rules[tag] += 1

    freq_dist_rules_list = []
    for k in freq_dist_rules:
        freq_dist_rules_list.append((k,freq_dist_rules[k]))
    freq_dist_rules_list.sort(key=lambda tup: tup[1], reverse=True) 

    
    print("Scanning Rules...")
    for rule in rules:
        rule_score = scoreRule_A(rule,freq_dist_rules_list,mean_sent_size)
        best_rules.append((rule,rule_score))
        best_rules.sort(key=lambda tup: tup[1]) 
        if len(best_rules) > 10:
            best_rules = best_rules[1:]
            
            
    # RUN PARAMERS        
    iterations = 10
    subject_range = 15
    n_best_sent = 30
  
        
    print('Finding subject...')
    subject = common_nouns_list_nnp[-subject_range:][int(random.random()*subject_range)]
    
    rule_idx = 0;
    si = 1
    print("Sentence Gen...")
    while si <= iterations:
        si += 1
        for rule in best_rules:
            print(rule_idx,end=' ')
            rule_idx+=1
            
            s = applyPOSBigrams(rule[0],bigrams);
            s = applyTrigrams(s,trigrams);
            s =  applyTrigramsSubjectMatch(s, trigrams, subject)
            s = applyBigramsSubjectMatch(s, bigrams, subject)
            fease, fgrade, length = scoreSentence(s,d)
            
            score = fease - fgrade 
            
            best_sentences.append((s,score,rule))
            best_sentences.sort(key=lambda tup: tup[1]) 
            
            if len(best_sentences) > n_best_sent:
                best_sentences = best_sentences[1:]

#    for s in best_sentences:
#        print(outputSentence(s[0]))
#        print(s[1])
#        print(s[2])
#        print()



    print()
    # Build sentence
    setences_in_paragraph = 5
    indexes = [i for i in range(0, n_best_sent)];
    random.shuffle(indexes)

    print('Subject: '+ subject[0].split()[0] + '\n')
    abstract = '    '     
    for i in range(0 , setences_in_paragraph):
        abstract += outputSentence(best_sentences[i][0],subject[0].split()[0]) + ' ';
        
    
    print(abstract)


if __name__ == '__main__':
    main()
