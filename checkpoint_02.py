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
import os
import pandas as pd
import re
import time

from checkpoint_01 import DICTIONARY_OUTPUT

# Variables
HOME = 'D:\cis_536' # Change to corpus directory

DICTIONARY_OUTPUT = 'dictionary2.txt'
UNIGRAM_BASE = 'unigrams2_'
CHUNK_SIZE = 104857600 # 100 MB
chunk_count = 0 # Combine this with UNIGRAM_BASE to name local inverted indices
ii_file = f'{UNIGRAM_BASE}{chunk_count}.txt' # update, reuse

REMOVE_REGEX = ["https:\/\/[^\s]+\s", "#lt.+#gt", "'[a-z]+", "[^\s\w]", "_", "[0-9]+[a-z]+", "[0-9]", "[ \t]{2,}"]
DOC_ID_REGEX = "curid=[\d]+"

STOP_WORDS = ['be', 'the', 'of', 'a', 'in', 'and', 'to', 'as', 'for', 'from', 'on', 'have', 'it', 'with', 'by', 'one', 'he', 'at', 'an', 'during', 'who', 'his', 'also', 'that', 'this', 'which', 'after', 'between', 'its', 'their', 'but', 'until', 'or', 'into', 'over', 'then', 'up']

prev = ''

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
                process(text)

# Directory navigation
# In the indicated folder
# Loop through each of the files

# Map
def process(words):
    """
    :param words: String of text
    :return:
    """
    
# Extract the doc-id (toss the curid=)
# remove anything unwanted
# lowercase, then lemmatize each word
# check if word is already in vocab
# ignore if stop word
# put into dictionary of doc-id, tf

# Reduce

# Write to file