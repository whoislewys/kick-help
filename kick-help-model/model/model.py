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
print(word_embeddings_path)


def scrape_from_csv(dataset_path):
    # open data
    X = []
    Y = []
    with open(dataset_path, 'r') as csvfile:
        dataset1 = csv.reader(csvfile)
        # iterate through projects
        for counter, row in enumerate(dataset1):
            text_label = row[9]  # possible values: success, failed, canceled (sic)
            if counter == 0 or text_label == 'canceled': # ignore csv categories and canceled projects
                continue
            elif counter == 10:
                break
            name = row[1]
            name_pattern = re.compile(name)
            search = requests.get('http://www.kickstarter.com/projects/search.json?search=&term={}'.format(name))
            search_response = search.json()
            for project in search_response['projects']:
                if name_pattern.match(project['name']): # search for project name that matches dataset name
                    # scrape
                    project_url = project['urls']['web']['project']
                    scrape_results = scrape_from_url(project_url)
                    X.append(scrape_results)
                    num_label = label_to_number(text_label)
                    Y.append(num_label)
    return X, Y


def scrape_from_url(project_url):
    # init dictionary
    data = {'category': '',
            'blurb': '',
            'title': '',
            'duration': '',
            'goal': '',
            'raised': '',
            'description': '',
            'risks': '',
            'name': ''}
    # get html tree
    page = requests.get(project_url)
    tree = html.fromstring(page.content)
    # get content
    try:
        data['category'] = tree.xpath('//a[@class="nowrap navy-700 flex items-center medium mr3 type-12"]/text()')[0]
    except:
        pass
    try:
        data['title'] = tree.xpath('//div[@class="col-20-24 col-lg-15-24 hide block-md order-2-md"]//h2/text()')[0]
    except:
        pass
    try:
        data['blurb'] = tree.xpath('//div[@class="col-20-24 col-lg-15-24 hide block-md order-2-md"]//p/text()')[0]
    except:
        pass
    try:
        time1 = tree.xpath('//div[@class="NS_campaigns__funding_period"]//p//time[1]/@datetime')[0]
        time2 = tree.xpath('//div[@class="NS_campaigns__funding_period"]//p//time[2]/@datetime')[0]
        data['duration'] = get_duration(time1, time2)
    except:
        pass
    try:
        data['goal'] = tree.xpath('//div[@id="pledged"]/@data-goal')[0]
    except:
        pass
    try:
        data['raised'] = tree.xpath('//div[@id="pledged"]/@data-pledged')[0]
    except:
        pass
    try:
        data['description'] = ''.join(tree.xpath('//div[@class="full-description js-full-description responsive-media formatted-lists"]//p/text()'))
        # text_to_word_sequence(data['description'])
    except:
        pass
    try:
        data['risks'] = ''.join(tree.xpath('//div[@class="mb3 mb10-sm mb3 js-risks"]//p/text()'))
    except:
        pass
    try:
        data['name'] = tree.xpath('//a[@class="medium navy-700 remote_modal_dialog"]/text()')[0]
    except:
        pass
    # clean
    for key in data:
        data[key] = data[key].replace('\n', ' ').strip()

    # words per line

    return data


def label_to_number(text_label): # text_label is success=0, failed=1, canceled=2 (sic)
    if text_label == 'successful':
        num_label = 0
    elif text_label == 'failed':
        num_label = 1
    elif text_label == 'canceled':
        num_label = 2
    return num_label


def get_duration(time1, time2):
    # convert string to datetime
    t1 = datetime.strptime(time1[0:18], '%Y-%m-%dT%H:%M:%S')
    t2 = datetime.strptime(time2[0:18], '%Y-%m-%dT%H:%M:%S')
    # get delta
    t3 = t2 - t1
    # return
    return(str(t3.total_seconds()))


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
    print('Loaded %s word vectors.' % len(embeddings_index))

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
    print(X)
    X = pad_sequences(X, maxlen=12)
    y = [1, 0, 0, 0, 0]


    model = Sequential()
    model.add(embedding_layer)
    model.add(Flatten())
    model.add(Dense(1, activation='sigmoid'))
    model.layers[0].trainable=False
    model.compile(loss='binary_crossentropy', optimizer='rmsprop')
    # eventually use x_train instead of placeholder X
    model.fit(X, y=y, batch_size=20, epochs=700, verbose=0, validation_split=0.2, shuffle=True)
    model.predict(X)

if __name__ == '__main__':
    embeddings_index = load_word2vec_embeddings()
    train_x, train_y = scrape_from_csv(dataset_path=dataset1_path)
    print("Data: {}\nLabels: {}".format(train_x, train_y))
    train(train_x, train_y)

    # test_x, test_y = scrape_from_csv(dataset_path=dataset1_path)

'''
how to pretty print json:
print(json.dumps(<JSON_DATA>, indent=2))
'''