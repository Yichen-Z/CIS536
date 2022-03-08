"""
Project checkpoint 1

Input:
txt file of Wikipedia text, starting with URLs, and tags denoted as #gt, #lt

Output:
Dictionary/vocabulary in alphabetical order
Words by number of documents they appear in (and then by their frequency across documents)

Yichen Zhang
CIS 536
Spring 2022
Last updated: 3/7/2022
"""

import os # For filepath and directory manipulation
import re # Regex
# from click import edit
import pandas as pd # To create and manipulate data in dataframes
from functools import reduce # Used to combine 3 dataframes (vocabulary, doc freq, word count) into one on the column 'word'
import spacy # Open-source package for lemmatizing (and tokenizing)
import time # To track how long the lemmatization takes

# -------------------------------------------
# Variables
# -------------------------------------------
HOME = 'D:\cis_536' # Change this to the directory where the original txt file resides
FILE = 'tiny_wikipedia_copy.txt' # Change this to the original txt file name
FILEPATH = os.path.join(HOME, FILE) 
ROWS = 100  # Change this for number of lines to pull from the full original file
SAMPLE_FILE = 'sample_wikipedia.txt'  # sample txt file created with the designated number of rows above
CLEAN_FILE = 'cleaned_wikipedia.txt' # This is the cleaned and lemmatized file


DICTIONARY_OUTPUT = 'dictionary.txt'
UNIGRAM_OUTPUT = 'unigrams.txt'

# regex for find and replace to clean the text data
remove_regex = ["https:\/\/[^\s]+\s", "#lt.+#gt", "'[a-z]+", "[^\s\w]", "_", "[0-9]+[a-z]+", "[0-9]", "[ \t]{2,}"]

word_count = {}
doc_freq = {}

# -------------------------------------------
# Methods
# -------------------------------------------
def sample_text(filepath):
    with open(filepath, 'r') as input, open(SAMPLE_FILE, 'w', newline='') as output:
        sample = input.readlines()
        output.writelines(sample[0:ROWS])

def change_to_lowercase(filepath):
    with open(filepath, 'r+') as input:
        file = input.read()
        file = file.lower()
        input.seek(0)
        input.write(file)

def regex_replace(regex_list = remove_regex, replace = ' ', filepath = SAMPLE_FILE):
    with open(filepath, 'r+') as input_file:
        file = input_file.read()
        for find_regex in regex_list:
            file = re.sub(find_regex, replace, file)
        input_file.seek(0)
        input_file.write(file)
        input_file.truncate() # very important, or weird previous lines of text linger

def lemmatize_file(input_file = SAMPLE_FILE, output_file = CLEAN_FILE):
    start = time.time()
    nlp = spacy.load('en_core_web_sm') # small English model

    with open(input_file, 'r') as in_file, open(output_file, 'w', newline='', encoding='utf-8') as out_file:
        output_string = ''
        input_lines = in_file.readlines()
        with nlp.select_pipes(disable=['parser', 'ner']): # only use the pipelines needed to lemmatize to save time
            docs = list(nlp.pipe(input_lines)) # use spaCy stream for faster conversion and processing. Very important. This and above line cut processing time from 800+ sec to under 4 sec
            for doc in docs:
                lemmatized_text = ' '.join([token.lemma_ for token in doc]).lower() # to prevent auto-capitalization of pronoun 'I'
                output_string += lemmatized_text
        out_file.write(output_string)
    
    end = time.time()
    print('Lemmatization time: ', end - start)

"""
Makes the vocabulary text file
Also populates the word count
"""
def make_corpus_dictionary(vocabulary_file=DICTIONARY_OUTPUT, filepath=CLEAN_FILE):
    with open(filepath, 'r') as input_file, open(vocabulary_file, 'w') as output_file:
        words = input_file.read()
        word_dump = words.split()
        vocabulary = []
        index = 0

        for word in word_dump:
            if word not in vocabulary and word != '':
                vocabulary.append(word)
                word_count[word] = 1
            elif word != '':
                word_count[word] += 1

        vocabulary.sort()

        # Write to vocabulary file
        for word in vocabulary:
            output_file.write(str(index) + ' ' + word + '\n')
            index += 1

"""
Turns word count dictionary into a dataframe
"""      
def count_words():
    df = pd.DataFrame(list(word_count.items()))
    df.columns = ['word', 'count']
    # print(df.head(5))
    return df

"""
Populates the document frequency dictionary
"""
def count_doc_freq(filepath = CLEAN_FILE):
    with open(filepath, 'r') as input:
        for line in input:
            unique = set(line.split(' '))
            for word in unique:
                if word not in doc_freq and word != '':
                    doc_freq[word] = 1
                elif word != '':
                    doc_freq[word] += 1
    
    df = pd.DataFrame(list(doc_freq.items()))
    df.columns = ['word', 'doc_freq']
    # print(df.head(5))
    return df

"""
Builds unigram model output file
Combines vocabulary list, document frequency, and global term frequency (word count)
"""
def build_unigram(input_file = DICTIONARY_OUTPUT, output_file = UNIGRAM_OUTPUT):
    vocab = pd.read_csv(input_file, header=None, delimiter=' ')
    vocab.columns = ['code', 'word']

    # Only dictionary entries - ID, word
    # print(vocab.head(5))

    dataframes = [vocab, count_doc_freq(), count_words()]
    combined_df = reduce(lambda left, right: pd.merge(left, right, on = 'word'), dataframes)

    combined_df.sort_values(by = ['doc_freq', 'count'], ascending = False, inplace=True, ignore_index=True)

    # Check
    # print(combined_df.head(5))

    with open(output_file, 'w', newline='', encoding='utf-8') as out_file:
        combined_df.to_csv(out_file, index = None, sep=' ')

    return combined_df

# -------------------------------------------
# Putting it together
# -------------------------------------------
"""
Creates a smaller text file of the first ROWS from the original full tiny_wikipedia.txt
Done
To improve: randomize sample
"""
sample_text(FILEPATH)

"""
Clean data
"""
change_to_lowercase(SAMPLE_FILE)
regex_replace()

# Lemmatize words
lemmatize_file()

"""
Create corpus vocabulary/dictionary file
"""
make_corpus_dictionary()
build_unigram()
