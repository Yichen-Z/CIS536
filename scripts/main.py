import os
import time

CORPUS = r'D:\cis_536\wikidata_small_test'
OUTPUT_FOLDER = r'C:\Users\house\workspace\CIS_536_TextMining\outputs'

## Run!

def run():
    make_vocabulary
    make_indices

def make_vocabulary(path):
    """
    <word-id> <word> in alphabetical order
    """
    if(os.path.isdir(path)):
        # Loop through, deal with each file
    elif(os.path.isfile(path)):
        try:
            # Deal with one file
        except:
            print(f'{path} not a readable file') 
    

def make_indices():
    """
    <word-id> <word> <doc-freq> (doc-id, tf) (doc-id, tf) ...
    :return: None
    """