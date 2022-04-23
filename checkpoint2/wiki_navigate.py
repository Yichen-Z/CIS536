"""
Navigate through wikipedia text files for a first-pass cleaning of text data
"""

import os
import re
import spacy

REMOVE_REGEX = [r"https:\/\/[^\s]+\s", r"^\n", r"^\r\n", r"'[a-z]+", r"[^\s\w]", "_", r"\d+"]
DOC_REGEX = re.compile(r'^https://en.wikipedia.org/wiki\?curid=(.*?)\s')
PATTERN = re.compile(r"(" + '|'.join(REMOVE_REGEX) + r")")
SPACES = re.compile(r"[\s]{2,}")

nlp = spacy.load('en_core_web_sm')

def navigate(path, wpath):
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            navigate(item_path, wpath)
        else:
            item = os.path.join(path, item)
            try:
                process(item, wpath)
            except Exception as e:
                print(f'{item} error: {e}')
                continue

def process(read_path, write_folder):
    with open(read_path, mode='r', encoding='utf-8') as rf:
        for line in rf:
            try:
                clean_line(line, write_folder)
            except Exception as e:
                print(f'Error: {e}')
                continue
        
def clean_line(t, wpath):
    wname = get_docID(DOC_REGEX, t)
    with open(os.path.join(wpath, wname + '.txt'), mode='w', newline='', encoding='utf-8') as wf:
            wf.write(clean(PATTERN, t))

def clean(regex_pattern, text, replace = ' '):
    return SPACES.sub(replace, lemmatize(regex_pattern.sub(replace, text))).strip()

def lemmatize(text):
    lt = ''
    with nlp.select_pipes(disable=['parser','ner']):
        doc = nlp(text)
        lt += ' '.join([token.lemma_ for token in doc])
    return lt

def get_docID(regex_pattern, text):
    return re.match(regex_pattern, text).group(1)