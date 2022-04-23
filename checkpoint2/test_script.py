"""
Testing parts of building a bigger set of inverted indices
"""
import os
import re
import spacy
import time

CHUNK_SIZE = 104857600
big_file = r'D:\cis_536\wikidata\wikidata.000000'
rfile = r'D:\cis_536\wikidata_small_test\wikidata.000000'
tiny_file = r'D:\cis_536\wikidata_small_test\tiny.txt'
output_folder = r'C:\Users\house\workspace\outputs'

BLANKS = [r"^\n", r"https:\/\/[^\s]+curid="]
REMOVE_REGEX = [r"'[a-z]+", r"[^\s\w]", "_"]
    # , r'[\s]be[^\w]',  r'[\s]the[^\w]',  r'[\s]a[^\w]',  r'[\s]an[^\w]',  
    # r'[\s]have[^\w]',  r'[\s]of[^\w]',  r'[\s]from[^\w]',  r'[\s]in[^\w]',  r'[\s]and[^\w]',  r'[\s]but[^\w]',
    #  r'[\s]to[^\w]',  r'[\s]on[^\w]',  r'[\s]for[^\w]']
    # r'[\s][Ii]s[^\w]', r'[\s][Tt]he[^\w]', 
    # r'[\s][Oo]f[^\w]', r'[\s][Aa][^\w]', r'[\s][Aa]m[^\w]',  r'[\s][Bb]e[^\w]',
    #  r'[\s][Aa]re[^\w]',  r'[\s][Ww]ere[^\w]',  r'[\s][Ww]as[^\w]',
    # r'[\s][Ii]n[^\w]', r'[\s][Aa]nd[^\w]', r'[\s][Tt]o[^\w]', r'[\s][Aa]s[^\w]',
    # r'[\s][Ff]or[^\w]', r'[\s][Ff]rom[^\w]', r'[\s][Oo]n[^\w]', r'[\s][Hh]ave[^\w]',
    #  r'[\s][Bb]een[^\w]',  r'[\s][Hh]as[^\w]',  r'[\s][Hh]ad[^\w]',  r'[\s][Aa]n[^\w]']
    # r'[\s]it[^\w]', r'[\s]with[^\w]', r'[\s]by[^\w]', r'[\s]one[^\w]', 
    # r'[\s]he[^\w]', r'[\s]at[^\w]', r'[\s]an[^\w]', r'[\s]during[^\w]',
    # r'[\s]she[^\w]', r'[\s]I[^\w]', r'[\s]we[^\w]', r'[\s]they[^\w]',
    # r'[\s]you[^\w]', r'[\s]him[^\w]', r'[\s]me[^\w]', r'[\s]her[^\w]', 
    # r'[\s]us[^\w]', r'[\s]them[^\w]', r'[\s]who[^\w]', r'[\s]also[^\w]',
    # r'[\s]that[^\w]', r'[\s]this[^\w]', r'[\s]which[^\w]', r'[\s]after[^\w]',
    # r'[\s]between[^\w]', r'[\s]its[^\w]', r'[\s]my[^\w]', r'[\s]mine[^\w]',
    # r'[\s]your[^\w]', r'[\s]yours[^\w]', r'[\s]their[^\w]', r'[\s]theirs[^\w]',
    # r'[\s]our[^\w]', r'[\s]ours[^\w]', r'[\s]his[^\w]', r'[\s]her[^\w]',
    # r'[\s]hers[^\w]', r'[\s]but[^\w]', r'[\s]until[^\w]', r'[\s]or[^\w]'
    # r'[\s]into[^\w]', r'[\s]over[^\w]', r'[\s]then[^\w]', r'[\s]up[^\w]']
blank_out = re.compile(r"(" + '|'.join(BLANKS) + r")")
pattern = re.compile(r"(" + '|'.join(REMOVE_REGEX) + r")")
spaces = re.compile(r"[ \t]{2,}")
STOP_WORDS = set(['be', 'the', 'of', 'a', 'in', 'and', 'to', 'as', 'for', 'from', 'on', 'have', 'it', 'with', 'by', 'one', 'he', 'at', 'an', 'during', 'who', 'his', 'also', 'that', 'this', 'which', 'after', 'between', 'its', 'their', 'but', 'until', 'or', 'into', 'over', 'then', 'up'])

def read_chunks(f, c=CHUNK_SIZE):
    """
        uses file.read() to read in text in chunks of size CHUNK_SIZE, set here to be 100 MB
        and process the documents in each line
        :param file: string for file path
        :param c: int for size of chunk to read
        :return:
        """
    part = ''
    while True:
        data = f.read(c)
        if not data:
            break
        yield data

def clean(words):
    return spacy_lemmatize(replace_regex(words))

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

def spacy_lemmatize(t):
    start = time.time()
    nlp = spacy.load('en_core_web_sm', disable =['parser', 'ner']) # small English model
    l_text = ''
    print("Starting lemmatization")
    for token in nlp(t):
        if token.lemma_ not in STOP_WORDS:
            l_text += token.lemma_ + ' '
    end = time.time()
    print('Spacy lemmatization time: ', end - start)
    return l_text.strip()

wname = 0
with open(rfile, 'r', encoding = 'utf-8') as f:
    start = time.time()
    for data in read_chunks(f):
        data = re.sub(blank_out, '', data)
        data = clean(data)
        wfile = os.path.join(output_folder, f'wikidata_{wname}.txt')
        with open(wfile, 'w', newline = '', encoding='utf-8') as w:
            w.write(data)
            wname += 1
            end = time.time()
            print(f'Finished {wfile} rewriting in {end - start} sec')

    