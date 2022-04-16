"""
CIS 536 Spring 2022
Yichen Zhang

This script can be run directly after installing dependencies
It can also forked from https://github.com/Yichen-Z/CIS536
"""

import csv
import os
import pandas as pd
import re
import spacy
import time

CORPUS = r'D:\cis_536\wikidata_small_test'
OUTPUT_FOLDER = r'C:\Users\house\workspace\CIS_536_TextMining\outputs'

df_docFreq = pd.DataFrame(columns = ['Term', 'DocFrequency'])
df_terms = pd.DataFrame(columns = [])
list_vocab = [] # sorting for proper indexing
dict_vocab = {} # term: [termID (-1 before sorting), df] 
    # termID: dict_vocab['term'][0] 
    # doc freq: dict_vocab['term'][1]
dict_by_doc = {} # term : [doc-id, tf]
    # dict_by_doc[word][0] returns doc-id
    # dict_by_doc[word][1] term frequency in that document
raw_list_by_doc = [] # list of dictionaries by document

# If not combined and compiled, RegEx will jam with large files
STOP_WORDS = ['be', 'the', 'of', 'a', 'in', 'and', 'to', 'as', 'for', 'from', 'on', 'have', 'it', 'with', 'by', 'one', 'he', 'at', 'an', 'during', 'who', 'his', 'also', 'that', 'this', 'which', 'after', 'between', 'its', 'their', 'but', 'until', 'or', 'into', 'over', 'then', 'up']
REMOVE_REGEX = [r"https:\/\/[^\s]+\s", r"'[a-z]+", r"[^\s\w]", "_"]
remove_stops = re.compile(r"(" + '|'.join(STOP_WORDS) + r")")
pattern = re.compile(r"(" + '|'.join(REMOVE_REGEX) + r")")
spaces = re.compile(r"[ \t]{2,}")
blank = re.compile(r"[\s\r\n]")
DOC_ID_REGEX = re.compile(r'curid=(\d+)')

# NLP model load
nlp = spacy.load('en_core_web_sm')

# Placeholder variables
d = '' # String for docID or anything else
v = {} # A good dictionary
start = time.time()
end = time.time()

def run():
    start = time.time()
    if os.path.isdir(CORPUS):
        map_corpus()
        set_termID()
        write_dict_to_file(dict_vocab, 'test_dictionary.txt')
    else:
        print(f'{CORPUS} is not a folder. Please choose a folder from which to read the text files.')
    end = time.time()
    print(f'Test concluded in {end - start} sec')

def map_corpus(folder = CORPUS):
    start = time.time()
    for file in os.listdir(folder):
        file = os.path.join(folder, file)
        raw_list_by_doc = [] # reset the list of term dictionaries by document
        with open(file, 'r', encoding='utf-8') as f:
            for line in f: # each line is a document
                if re.match(blank, line):
                    continue
                d = get_docID(line)
                line = clean(line)
                raw_list_by_doc.append(map_text(d, line))
        d = file.split('.')[-1] + '.txt'
        v = {} # Reduce: dict key-value pair by key-value pair --> new dict of dict term: {doc-id: tf}
        with open(d, 'w', newline='', encoding='utf-8') as raw_ii:
            for doc_dict in raw_list_by_doc:
                for word in doc_dict.keys():
                    v[word][doc_dict[word][0]] = doc_dict[word][1]
            writer = csv.writer(raw_ii)
            for key, value in v.items():
                writer.writerow([key, value])
    end = time.time()
    print(f'Writing raw postings by term: {end - start} sec')

# Helper functions
def clean(words):
    return replace_regex(remove_stops, lemmatize(replace_regex(pattern, words))) # spaCy lemmatizer also takes care of lowercasing when it makes sense


def get_docID(t):
    """
    :param t: String text through which to search with DOC_ID_REGEX
    :return: String docID
    """
    result = re.search(DOC_ID_REGEX, t)
    return result.group(1)

def lemmatize(text):
    """
    :param text: String
    :return: String lemmatized (and lowercase where appropriate)
    """
    start = time.time()
    l_text = ''
    with nlp.select_pipes(disable=['parser','ner']):
        docs = list(nlp.pipe(text))
        for doc in docs:
            l_text += ' '.join([token.lemma_ for token in doc])
    end = time.time()
    print(f'Lemmatization: {end - start} sec')
    return l_text

def map_text(docID, doc):
    """
    Also calls update_vocab
    :param docID: String
    :param doc: String of words
    :return: dict 'term': [docID: tf] all words in doc
    """
    start = time.time()
    v = {} # reset placeholder dict
    for word in doc.split():
        if word not in v:
            v[word] = [docID, 1]
        else:
            v[word][1] += 1
    for word in v:
        update_vocab(word)
    end = time.time()
    print(f'Mapping text and updating vocab: {end - start} sec')
    return v

def replace_regex(regex_to_replace, text, r = ' '):
    """
    :param text: String
    :param l: list of regex for replacing (note that last has to replace multiple consecutive spaces)
    :param r: replace with one space
    :return: String all replaced
    """
    # for find in REMOVE_REGEX: # this is really slow
    #     find = re.compile(find)
    print('Starting regex replace')
    start = time.time()
    text = regex_to_replace.sub(r, text)
    end = time.time()
    print(f'Replacing text: {end - start} sec. Now removing excess whitespaces.')
    return spaces.sub(r, text)

def update_vocab(w):
    if w not in dict_vocab.keys():
        dict_vocab[w] = [-1, 1] # placeholder termID, then start doc freq count
        list_vocab.append(w)
    else:
        dict_vocab[w][1] += 1 # just update doc freq count

def write_dict_to_file(dictionary, fpath):
    with open(fpath, 'w', newline='', encoding='utf-8') as wfile:
        writer = csv.writer(wfile)
        for key, value in dictionary.items():
            writer.writerow([key, value])

# Vocabulary compilation
def set_termID(lv = list_vocab, dv = dict_vocab):
    """
    Sorts the list of terms, and iterates through dictionary, updating termID
    Where termID is dict_vocab['term'][0]
    :param lv: list of terms
    :param dv: dict 'term': [termID, document frequency]
    """
    start = time.time()
    lv.sort() # This can be slow
    id = 0
    for word in lv:
        if word not in dv.keys():
            print(f'List/Dict mismatch: {word} not found in dictionary. Continuing.')
            continue
        else:
            dv[word][0] = id
            id += 1 # This can get very big
    end = time.time()
    print(f'vocab ordered and indexed: {end - start} sec')

# Test
run()