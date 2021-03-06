from regex import R
import checkpoint_02 as c
import os
import time

big_files = [r'D:\cis_536\wikidata\wikidata.000039', r'D:\cis_536\wikidata\wikidata.000009']
small_files = r'D:\cis_536\wikidata_small'
big_file = r'D:\cis_536\wikidata\wikidata.000000'
output_folder = r'C:\Users\house\workspace\outputs'
tiny_file = r'D:\cis_536\wikidata_small_test\tiny.txt'

# # Test chunk reading - hangs with spaCy
# start = time.time()
# c.read_chunks(r'D:\cis_536\wikidata\wikidata.000039')
# end = time.time()
# print(c.vocab)
# print(f'Testing read_chunks takes {end - start} sec')

# # test map_text
# i = '1403'
# w = 'sunshine grace world today today sunshine sunshine'
# print(c.map_text(i,w))
# # output: {'sunshine': {'1403': 3}, 'grace': {'1403': 1}, 'world': {'1403': 1}, 'today': {'1403': 2}}

# test get_docID
# w = 'dlafalsdkjfcurid=133 the world is great'
# print(c.get_docID(w))

# # test replace_regex
w = r'https://en.wikipedia.org/wiki?curid=858197 Astra ( 1954 automobile ) the wonders are The Wonders'
# print(c.replace_regex(w))

# test clean()
start = time.time()
print(c.clean(w))
end = time.time()
print(f'cleaning text done in {end - start}')

# test everything so far

## Stage 1: One small file


# start = time.time()
# c.write_vocab('tiny_vocabulary.txt')
# end = time.time()
# print(f'Tiny vocabulary writes to file in {end - start} secs')

# start = time.time()
# c.write_index(raw, 'tiny_inverted_index.txt')
# end = time.time()
# print(f'Tiny inverted index writes in {end - start} secs')

## Stage 2: Multiple small files
# def end_to_end():
#     for file in os.listdir(small_files):

# start = time.time()
# print(c.vocab)
# c.read_file(file)
# print(c.vocab)
# end = time.time()
# print(f'Cleaning and ignoring stop words takes {end - start} sec')