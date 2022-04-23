"""
Project checkpoint 2

Input:
folder containing files of Wikipedia text, starting with URLs, and tags denoted as #gt, #lt

Output:
Dictionary/vocabulary in alphabetical order
Local inverted indices for every chunk of text data
    Ignore stop words identified in checkpoint 1
    Format: word-code word doc-freq (doc-id, tf) (doc-id, tf) ...
        Ascending word-code order
    Submit 2, not all needed
Other potential stats of interest
    Document lengths
    Corpus document count

Yichen Zhang
CIS 536
Spring 2022
Last updated: 4/14/2022
"""

# Imports
import csv
import os
import pandas as pd
import re
import spacy
import time

# Variables
OUTPUTS = r'C:\Users\house\workspace\CIS_536_TextMining\outputs' # Change to where the indices will be written
inputs = [r'D:\cis_536\wikidata\wikidata.000039', r'D:\cis_536\wikidata\wikidata.000009']

DICTIONARY_OUTPUT = 'dictionary2.txt'
UNIGRAM_BASE = 'unigrams2_'

# Took out "#lt.+#gt" from Checkpoint_1 since the tags do not appear in the new files
# Took out "[0-9]+[a-z]+", "[0-9]" to keep the numbers in the text
REMOVE_REGEX = [r"https:\/\/[^\s]+\s", r"'[a-z]+", r"[^\s\w]", "_"]
pattern = re.compile(r"(" + '|'.join(REMOVE_REGEX) + r")")
spaces = re.compile(r"[ \t]{2,}")
DOC_ID_REGEX = r'curid=(\d+)'
STOP_WORDS = set(['be', 'the', 'of', 'a', 'in', 'and', 'to', 'as', 'for', 'from', 'on', 'have', 'it', 'with', 'by', 'one', 'he', 'at', 'an', 'during', 'who', 'his', 'also', 'that', 'this', 'which', 'after', 'between', 'its', 'their', 'but', 'until', 'or', 'into', 'over', 'then', 'up'])

start = time.time()
end = time.time()

vocab = {}
v = {} # placeholder dictionary
d = '' # placeholder string
raw_list = []
chunk_index = {}

nlp = spacy.load('en_core_web_sm')

# File input
def do_everything(folder = inputs):
    temp_list = []
    for f in folder: # each file to process
        temp_list = read_file(f)

# Map
def read_file(fpath):
    raw_list = []
    with open(fpath, 'r', encoding='utf-8') as f:
        for line in f: # each line is a document > get back dict of terms and single-doc counts > want compile by term
            raw_list.append(process(line))
    return raw_list

def process(words):
    """
    :param words: String - a line of text
    :return: dict 'term': {docID: tf}
    """
    d = get_docID(words)
    return map_text(d, clean(words))

def get_docID(t):
    """
    :param t: String text through which to search with DOC_ID_REGEX
    :return: String docID
    """
    result = re.search(DOC_ID_REGEX, t)
    return result.group(1)

def map_text(docID, doc):
    """
    Also updates universal vocabulary
    :param docID: String
    :param doc: String of words
    :return: dict 'term': {docID: count of word in doc}
    """
    v = {} # reset placeholder dict
    for word in doc.split():
        if word not in vocab:
            vocab[word] = 1 # placeholder for termID for now
        if word not in STOP_WORDS:
            if word not in v:
                v[word] = {docID: 1}
            else:
                v[word][docID] += 1
    return v

def clean(words):
    return replace_regex(lemmatize(words)) # spaCy lemmatizer also takes care of lowercasing when it makes sense

def replace_regex(text, r = ' '):
    """
    :param text: String
    :param l: list of regex for replacing (note that last has to replace multiple consecutive spaces)
    :param r: replace with one space
    :return: String all replaced
    """
    # for find in REMOVE_REGEX: # this is really slow
    #     find = re.compile(find)
    print('Starting regex replace')
    text = pattern.sub(r, text)
    return spaces.sub(r, text)

def lemmatize(text):
    """
    Differs from Checkpoint 1's since this goes line by line
    :param text: String
    :return: String lemmatized (and lowercase where appropriate)
    """
    l_text = ''
    with nlp.select_pipes(disable=['parser','ner']):
        docs = list(nlp.pipe(text))
        for doc in docs:
            l_text += ' '.join([token.lemma_ for token in doc])
    return l_text

# Reduce
def reduce_list(postings):
    chunk_index = {}
    for post in postings:
        for word in post:
            if word not in chunk_index.keys():
                chunk_index[word] = []
            chunk_index[word].append(post[word])
    return chunk_index

# Write to file
def write_vocab(fpath = DICTIONARY_OUTPUT):
    ti = 0
    with open(fpath, 'w') as out_file:
        for word in list(vocab.keys()).sort():
            vocab[word] = ti
            ti += 1
            out_file.write(f"{str(vocab[word])} {word}")


def write_index(raw_index, wfile, v = vocab):
    """
    Writes the "localized" inverted indices to file (here .txt)
    :param raw_index: dict 'term': {{doc-id: tf} ...}
    :param wfile: String filepath for file to write to
    :param vocab: dict 'term': 'term-id'
    :return: None
    """
    with open(wfile, 'w', newline='', encoding='utf-8') as outfile, open(vocab, 'r') as v:
        writer = csv.writer(outfile, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
        for key, value in raw_index.items():
            writer.writerow([vocab[key], key, value])