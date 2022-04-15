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
from functools import partial
import csv
import os
import pandas as pd
import re
import time

# Variables
HOME = r'D:\cis_536\outputs' # Change to corpus directory

DICTIONARY_OUTPUT = 'dictionary2.txt'
UNIGRAM_BASE = 'unigrams2_'
CHUNK_SIZE = 104857600 # 100 MB
chunk_count = 0 # Combine this with UNIGRAM_BASE to name local inverted indices
ii_file = f'{UNIGRAM_BASE}{chunk_count}.txt' # update, reuse

# Took out "#lt.+#gt" from Checkpoint_1 since the tags do not appear in the new files
# Took out "[0-9]+[a-z]+", "[0-9]" to keep the numbers in the text
REMOVE_REGEX = [r"https:\/\/[^\s]+\s", r"'[a-z]+", r"[^\s\w]", "_", r"[ \t]{2,}"]
DOC_ID_REGEX = r'curid=(\d+)'

STOP_WORDS = ['be', 'the', 'of', 'a', 'in', 'and', 'to', 'as', 'for', 'from', 'on', 'have', 'it', 'with', 'by', 'one', 'he', 'at', 'an', 'during', 'who', 'his', 'also', 'that', 'this', 'which', 'after', 'between', 'its', 'their', 'but', 'until', 'or', 'into', 'over', 'then', 'up']

prev = ''

start = time.time()
end = time.time()

vocab = {}
v = {} # placeholder dictionary

# File input
# Read in chunks of 100 MB
def read_chunks(file, c = CHUNK_SIZE):
    """
    uses file.read() to read in text in chunks of size CHUNK_SIZE, set here to be 100 MB
    and process the documents in each line
    :param file: string for file path
    :param c: int for size of chunk to read
    :return:
    """
    with open(file, 'r', encoding='utf-8') as f:
        rfile = partial(f.read, c)
        for text in iter(rfile, ''): # stop when the file ends
            if not text.endswith('\n'): # catching part of the last line that we can read
                prev = text
            else:
                if prev != '': # there's a lingering partial line
                    text = prev + text
                    prev = ''
                # this is a complete line and can be processed as usual
                # process(text)

# Directory navigation
# In the indicated folder
# Loop through each of the files

# Map
def process(words):
    """
    :param words: String - a line of text
    :return:
    """
    get_docID(words)

def get_docID(t):
    """
    :param t: String text through which to search with DOC_ID_REGEX
    :return: String docID
    """
    result = re.search(DOC_ID_REGEX, t)
    return result.group(1)
    # return re.sub(DOC_ID_REGEX, '', result.group(1))

def map_text(docID, doc):
    """
    :param docID: String
    :param doc: String of words
    :return: dict 'term': {docID: count of word in doc}
    """
    v = {} # reset placeholder dict
    for word in doc.split():
        if word not in v:
            v[word] = {docID: 1}
        else:
            v[word][docID] += 1
    return v

# Extract the doc-id (toss the curid=)
# remove anything unwanted
# lowercase, then lemmatize each word
# check if word is already in vocab
# ignore if stop word
# put into dictionary of doc-id, tf

# Reduce

# Write to file


def write_index(raw_index, wfile, vocab):
    """
    Writes the "localized" inverted indices to file (here .txt)
    :param raw_dictionary: dict 'term': {{doc-id: tf} ...}
    :param wfile: String filepath for file to write to
    :param vocab: dict 'term': 'term-id'
    :return: None
    """
    with open(wfile, 'w', newline='', encoding='utf-8') as outfile, open(vocab, 'r') as v:
        writer = csv.writer(outfile, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
        for key, value in raw_index.items():
            writer.writerow([vocab[key], key, value])