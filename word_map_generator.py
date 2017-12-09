from gensim.models import Word2Vec
import os
import numpy as np

class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                yield [line.strip()]

sentences = MySentences('/Users/Ruta/Desktop/Autolab/alphaclean/data_strings') # a memory-friendly iterator
# print(list(sentences))
model = Word2Vec(list(sentences), min_count=1)
# print(model['New Yorks'])

word_to_vec = {}

for sentence in sentences:
    word_to_vec[tuple(sentence)] = model[sentence]

# for k in word_to_vec:
#     print(k)
#     print(word_to_vec[k])
#     print("\n")

def vectorize(state):
    vector = []
    for k in state:
        v = state[k]
        inner_vec = []
        for val in v:
            key = tuple([val])
            # print(word_to_vec.keys())
            # print(key)
            assert key in word_to_vec.keys()
            inner_vec.append(word_to_vec[key])
        vector.append(inner_vec)
    return vector
