"""
Navigate through folders and subfolders for a first-pass cleaning of text data
Yichen Zhang
"""

import os
import re
import spacy
import time

HOME = r'D:\cis_536\maildir'
WRITE_DIR = r'C:\Users\house\workspace\email_outputs\with_punct'
messageID = re.compile(r'^Message-ID:\s<(.*?).JavaMail')
clean = re.compile(r"""^Message-ID[\w\W]+X-FileName: [^\n]+|----------------------[\w\W]+---------------------------|^To:[\w\W]+Subject:[^\n]+|^ -----Original Message-----|From:[^\n]+|Sent:[^\n]+|To:[^\n]+|Subject:[^\n]+|Cc:[^\n]+|Bcc:[^\n]+|<[^<>]*>|<[^<>]*\n+[^<>]*>|&nbsp;|'[\w]+\s""")
# punctuation = re.compile(r'_|[^\w\s\d]')
lines = re.compile(r'\n')
formatting = re.compile(r'<(.*?)>|= ')
blanks = re.compile(r'\s{2,}')

nlp = spacy.load('en_core_web_sm')

def navigate(path):
    """
    Go through every subfolder and file

    :param: path: a string for starting directory path
    """
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            navigate(item_path)
        else:
            # do something with the file
            print(item)
            item = os.path.join(path, item)
            try:
                process(item)
            except Exception as e:
                print(f'{item}: {e}')
                continue

def process(read_path, write_folder=WRITE_DIR):
    """
    Cleans

    :file: a string for path to a file
    """
    # open file, read text
    with open(read_path, mode='r', encoding='utf-8') as rfile:
        t = rfile.read()

        # Retain Message-ID and make into file id: <digits>.<digits>.JavaMail.person@thyme to <digits>_<digits>.txt
        wname = get_docID(messageID, t)
        
        # Strip metadata (mostly) and rewrite to one folder
        with open(os.path.join(write_folder, wname + '.txt'), mode='w', newline='', encoding='utf-8') as wfile:
            wfile.write(init_clean(clean, t))

def init_clean(clean_regex, text, replace = ' '):
    """
    Returns text from initial round of cleaning

    :param: clean_regex: regex pattern object to target what's to be replaced
    :param: text: string to be cleaned
    :param: replace: string of what will take the place of the matched parts, defaulting to empty
    :return: string cleaned
    """
    # start = time.time()
    t = clean_regex.sub(replace, text)
    t = lines.sub(replace, t)
    t = formatting.sub('', t)
    t = lemmatize(t)
    t = blanks.sub(' ', t)
    # end = time.time()
    # print(f'Text initially cleaned in {end - start} sec')
    return t

def lemmatize(text):
    """
    :param text: String
    :return: String lemmatized (and lowercase where appropriate)
    """
    # start = time.time()
    l_text = ''
    with nlp.select_pipes(disable=['parser','ner']):
        doc = nlp(text)
        l_text += ' '.join([token.lemma_ for token in doc])
    # end = time.time()
    # print(f'Lemmatization: {end - start} sec')
    return l_text

def get_docID(regex_pattern, text):
    """
    Returns numeric email ID <digits>_<digits>

    :param: text: a period-separated string <digits>.<digits>
    :return: _ separated string <digits>_<digits>
    """
    # Regex returns a match object
    # To get the string, use <match_object>.group(0) for entire matched text
    # Just the 1st capture - text of interest between the bookends - <match_object>.group(1) as used here
    parts = re.match(regex_pattern, text).group(1).split('.')
    return '_'.join(parts)

