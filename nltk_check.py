import nltk
from nltk.corpus import treebank
import os

HOME = 'D:\cis_536' # Change this to the directory where the original txt file resides
FILE = 'tiny_wikipedia_copy.txt' # Change this to the original txt file name
FILEPATH = os.path.join(HOME, FILE) 

t = treebank.parsed_sents(FILEPATH)[0]
t.draw()