import checkpoint_02 as c
import time

# Test chunk reading
# start = time.time()
# read_chunks(r'D:\cis_536\wikidata\wikidata.000039')
# end = time.time()
# print(f'Testing read_chunks takes {end - start} sec')

# # test map_text
# i = '1403'
# w = 'sunshine grace world today today sunshine sunshine'
# print(c.map_text(i,w))
# # output: {'sunshine': {'1403': 3}, 'grace': {'1403': 1}, 'world': {'1403': 1}, 'today': {'1403': 2}}

# # test get_docID
# w = 'dlafalsdkjfcurid=133 the world is great'
# print(c.get_docID(w))

# # test replace_regex
w = r'https://en.wikipedia.org/wiki?curid=858197 Astra ( 1954 automobile ) the wonders are The Wonders'
# print(c.replace_regex(w))

# # test clean()
# start = time.time()
# print(c.clean(w))
# end = time.time()
# print(f'cleaning text done in {end - start}')

# test everything so far
start = time.time()
print(c.vocab)
print(c.process(w))
print(c.vocab)
end = time.time()
print(f'Cleaning and ignoring stop words takes {end - start} sec')