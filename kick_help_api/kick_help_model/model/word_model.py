import os
import numpy as np

data_folder = os.path.join(os.pardir, 'data')
word_embeddings_path = os.path.join(data_folder, 'glove.6B', 'glove.6B.50d.txt')
# print(word_embeddings_path)

def load_word_model():
    # https://machinelearningmastery.com/develop-word-embeddings-python-gensim/
    # http://www.orbifold.net/default/2017/01/10/embedding-and-tokenizer-in-keras/
    word_model = {}
    glove_data = word_embeddings_path
    f = open(glove_data, encoding='utf-8')
    for line in f:
        values = line.split()
        word = values[0]
        embedding = np.array([float(val) for val in values[1:]])
        word_model[word] = embedding
    f.close()
    print('Loaded ' + str(len(word_model)) + ' word vectors.')
    return word_model

def get_word_values(text, word_model):
    word_values = []
    text = text.split()
    for word in text:
        try:
            word_values.append(word_model[word])
        except:
            pass
    return word_values