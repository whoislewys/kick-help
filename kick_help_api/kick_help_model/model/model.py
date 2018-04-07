import os
import numpy as np
import keras
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Flatten
from keras.layers.wrappers import TimeDistributed
from keras.layers.embeddings import Embedding
import word_model as wm
import sys
sys.path.append('C:\\Users\\lewys\\PycharmProjects\\kick-help\\kick_help_api\\')
import scrape


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
    # print('Loaded %s word vectors.' % len(embeddings_index))
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
    #print('\n', word_index)

    embedding_matrix = np.zeros((len(word_index) + 1, embedding_dimension))
    for word, i in word_index.items():
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            # words not found in embedding index will be all-zeros.
            embedding_matrix[i] = embedding_vector[:embedding_dimension]

    #Now you have an embedding matrix of 19 words into dimension 10:
    #print('Embedding matrix shape: ', embedding_matrix.shape)

    # define a new keras Embedding layer
    embedding_layer = Embedding(embedding_matrix.shape[0], embedding_matrix.shape[1], weights=[embedding_matrix], input_length=50)

    
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
    model.fit(x=train_x, y=train_y, batch_size=20, epochs=700, verbose=1, validation_split=0.2, shuffle=True)
    #model.predict()


if __name__ == '__main__':
    embeddings_index = load_word2vec_embeddings()
    # train_x, train_y = scrape_from_csv(dataset_path=dataset1_path)
    # print("Data: {}\nLabels: {}".format(train_x, train_y))
    num_classes = 2
    raw_train_data, raw_train_labels = scrape.scrape_from_csv(dataset1_path)

    features = np.empty((0, 50), dtype='float32')
    labels = np.empty(0, dtype=np.int)
    word_model = wm.load_word_model()
    for project in raw_train_data:
        description_values = (wm.get_word_values((project['description']), word_model))
        for description_value in description_values:
            #print(type(description_value))
            #print(description_value)
            parsed_features = np.hstack(description_value)
            features = np.vstack([features, parsed_features])

    train_x = np.array(features)
    train_y = keras.utils.to_categorical(raw_train_labels, num_classes)
    train(train_x, train_y)

    # test_x, test_y = scrape_from_csv(dataset_path=dataset1_path)

'''
how to pretty print json:
print(json.dumps(<JSON_DATA>, indent=2))
'''