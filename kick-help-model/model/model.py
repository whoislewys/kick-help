import os
import csv
import re
import requests
import json
from lxml import html
from datetime import datetime
import numpy as np
import keras
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Flatten
from keras.layers.wrappers import TimeDistributed
from keras.layers.embeddings import Embedding

# data_folder = os.path.join(os.getcwd(), '')
data_folder = os.path.join(os.pardir, 'data')
dataset1_path = os.path.join(data_folder, 'ks-projects-201612.csv')
dataset2_path = os.path.join(data_folder, 'ks-projects-201801.csv')
word_embeddings_path = os.path.join(data_folder, 'glove.6B', 'glove.6B.50d.txt')
# print(word_embeddings_path)

def load_word2vec_embeddings():
    # https://machinelearningmastery.com/develop-word-embeddings-python-gensim/
    # http://www.orbifold.net/default/2017/01/10/embedding-and-tokenizer-in-keras/
    embeddings_index = {}
    glove_data = word_embeddings_path
    f = open(glove_data, encoding='utf-8')
    for line in f:
        values = line.split()
        word = values[0]
        value = np.asarray(values[1:], dtype='float32')
        embeddings_index[word] = value
    f.close()
    print('Loaded %s word vectors.' % len(embeddings_index))
    return embeddings_index


def train(train_x, train_y):
    tokenizer = Tokenizer()  # allows you to prepare text in various ways for neural nets
    embeddings_index = {}
    glove_data = word_embeddings_path
    f = open(glove_data, encoding='utf-8')
    for line in f:
        values = line.split()
        word = values[0]
        value = np.asarray(values[1:], dtype='float32')
        embeddings_index[word] = value
    f.close()
    # print('Loaded %s word vectors.' % len(embeddings_index))

    texts = ["The sun is shining in June!", "September is grey.", "Life is beautiful in August.", "I like it", "This and other things?"]
    embedding_dimension = 10 # The embedding_matrix maps words to vectors in the specified embedding dimension (here 10):
    tokenizer.fit_on_texts(texts)
    word_index = tokenizer.word_index
    print('\n', word_index)

    embedding_matrix = np.zeros((len(word_index) + 1, embedding_dimension))
    for word, i in word_index.items():
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            # words not found in embedding index will be all-zeros.
            embedding_matrix[i] = embedding_vector[:embedding_dimension]

    #Now you have an embedding matrix of 19 words into dimension 10:
    print('Embedding matrix shape: ', embedding_matrix.shape)

    # define a new keras Embedding layer
    embedding_layer = Embedding(embedding_matrix.shape[0], embedding_matrix.shape[1], weights=[embedding_matrix], input_length=12)

    X = tokenizer.texts_to_sequences(texts)
    X = pad_sequences(X, maxlen=12)
    print(X)
    print(type(X))
    y = np.array([1, 0, 0, 0, 0])
    print(type(y))

    model = Sequential()
    model.add(embedding_layer)
    model.add(Flatten())
    model.add(Dense(1, activation='sigmoid'))
    model.layers[0].trainable=False
    model.compile(loss='binary_crossentropy', optimizer='rmsprop')
    # eventually use x_train instead of placeholder X
    model.fit(X, y=y, batch_size=20, epochs=700, verbose=1, validation_split=0.2, shuffle=True)
    model.predict(X)


if __name__ == '__main__':
    embeddings_index = load_word2vec_embeddings()
    # train_x, train_y = scrape_from_csv(dataset_path=dataset1_path)
    # print("Data: {}\nLabels: {}".format(train_x, train_y))
    train_x = ''
    train_y = ''
    train(train_x, train_y)

    # test_x, test_y = scrape_from_csv(dataset_path=dataset1_path)

'''
how to pretty print json:
print(json.dumps(<JSON_DATA>, indent=2))
'''