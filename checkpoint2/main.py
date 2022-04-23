"""
Sets directory paths
Creates vocabulary and inverted indices
"""
import wiki_navigate as nav
import wiki_vocab as wv

# RAW_FILES = r'D:\cis_536\wikidata' # RegEx and lemmatization both take too long for the full-sized 200 MB files
RAW_FILES = r'D:\cis_536\wikidata_small_test'
CLEANED_FILES = r'C:\Users\house\workspace\outputs_2'

# nav.navigate(RAW_FILES, CLEANED_FILES) # Probably best to try this one original Wikipedia file at a time

wv.make_index('small_index_2.txt', 'small_vocab_2.txt', CLEANED_FILES) # Need to separate the updating of the dictionary and the local indexes