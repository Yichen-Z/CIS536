import checkpoint_02 as c

# Test chunk reading
# start = time.time()
# read_chunks(r'D:\cis_536\wikidata\wikidata.000039')
# end = time.time()
# print(f'Testing read_chunks takes {end - start} sec')

# test map_text
i = '1403'
w = 'sunshine grace world today today sunshine sunshine'
print(c.map_text(i,w))
# output: {'sunshine': {'1403': 3}, 'grace': {'1403': 1}, 'world': {'1403': 1}, 'today': {'1403': 2}}