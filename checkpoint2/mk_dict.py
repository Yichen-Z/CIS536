"""
Map each document out to <doc-id> and word freq
"""
import os

HOME = r'C:\Users\house\workspace\email_outputs\with_punct'

punct_set = {'.', ',', '?', '!', r'~', r'`', r'#', r'$', r'%', r'^', r'&', r'*', r'(', r')', r'-', r'_', r'+', r'=', r'[', r']', r'{', r'}', r':', r';', r'"', r"'", r'<', r'>', r'|', r'\\', r'/'}

STOP_WORDS = set(['be', 'the', 'of', 'a', 'in', 'and', 'to', 'as', 'for', 'from', 'on', 'have', 'it', 'with', 'by', 'one', 'he', 'at', 'an', 'during', 'who', 'his', 'also', 'that', 'this', 'which', 'after', 'between', 'its', 'their', 'but', 'until', 'or', 'into', 'over', 'then', 'up'])

full_vocab = {}
vlist = []

def map(file, folder):
    """
    Helper for make_dictionary
    """
    v = {} # reset placeholder doc dictionary
    docID = get_docID(file)
    with open(os.path.join(folder, file), 'r', encoding='utf=8') as rfile:
        doc = rfile.read()
        for word in doc.split():
            if word not in punct_set:
                if word not in full_vocab:
                    full_vocab[word] = -1 # placeholder for termID
                    vlist.append(word)
                if word not in STOP_WORDS:
                    if word not in v:
                        v[word] = [docID, 1]
                    else:
                        v[word][1] += 1
    return v

def get_docID(file):
    return file.split('.')[0]

def make_dictionary(path):
    raw_list = []
    for file in os.listdir(path):
        try:
            raw_list.append(map(file, path))
        except Exception as e:
            print(f'{file} has error: {e}')
            continue
    return raw_list

def reduce(doc_vocabs_list):
    """
    
    :param: doc_vocabs_list: list of dictionaries by doc of the form <term> : {docID: count}
    :return: dictionary <term>: {docID: count}
    """
    inverted = {}
    for term_doc in doc_vocabs_list:
        for term, doc_post in term_doc.items():
            if term not in inverted:
                inverted[term] = {}
            inverted[term][doc_post[0]] = doc_post[1]
    return inverted

def map_reduce(dictionary_name = 'email_vocabulary_all.txt', path = HOME):
    # make dictionary and list of term counts by document
    list_by_doc = make_dictionary(path)

    # create dictionary with actual termIDs
    vlist.sort()
    count = 0
    with open(dictionary_name, 'w', encoding='utf-8') as wfile:
        for term in vlist:
            full_vocab[term] = count
            wfile.write(f'{count} {term}\n')
            count += 1
    
    # create inverted index with termID
    return reduce(list_by_doc)

def make_index(index_name = 'email_inverted_index_all.txt'):
    raw_index = map_reduce()
    with open(index_name, 'w', encoding='utf-8') as wfile:
        for term in vlist:
            if term in raw_index.keys():
                wfile.write(f'{full_vocab[term]} {term} {len(raw_index[term])} {raw_index[term]}\n')
