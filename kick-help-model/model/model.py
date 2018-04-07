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

def train(embeddings_index, train_x, train_y):
    '''
    We are assuming that effective kickstarter campaigns will have similar writing techniques
    So we will embed kickstarter data into ~10 dimensional vector spaces
    To make a prediction, we will either use a nearest neighbor algorithm (pribably much easier in these low dimensions) or a neural net
    '''

    # The embedding_matrix matrix maps words to vectors in the specified embedding dimension (here 10):
    embedding_dimension = 10
    tokenizer = Tokenizer() # allows you to prepare text in various ways for neural nets

    texts = ["The sun is shining in June!", "September is grey.", "Life is beautiful in August.", "I like it", "This and other things?"]
    tokenizer.fit_on_texts(texts)
    word_index = tokenizer.word_index

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


    # TODO: resolve missing word_index

    X = tokenizer.texts_to_sequences(texts)
    X = pad_sequences(X, maxlen=19)
    y = [1,0,0,0,0]
    vocab_size = len(tokenizer.word_index) + 1

    model = Sequential()
    model.add(Dense(2, input_dim=vocab_size))

    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='rmsprop')
    # eventually use x_train instead of placeholder X
    model.fit(X, y=train_y, batch_size=200, epochs=700, verbose=0, validation_split=0.2, shuffle=True)

if __name__ == '__main__':
    embeddings_index = load_word2vec_embeddings()
    train_x, train_y = scrape_from_csv(dataset_path=dataset1_path)
    print("Data: {}\nLabels: {}".format(train_x, train_y))
    preprocess(embeddings_index, train_x, train_y)
    train(embeddings_index, train_x, train_y)

    # test_x, test_y = scrape_from_csv(dataset_path=dataset1_path)

'''
how to pretty print json:
print(json.dumps(<JSON_DATA>, indent=2))
'''