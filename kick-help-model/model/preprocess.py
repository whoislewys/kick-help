data_folder = os.path.join(os.pardir, 'data')
word_embeddings_path = os.path.join(data_folder, 'glove.6B', 'glove.6B.50d.txt')
print(word_embeddings_path)

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


def preprocess(embeddings_index, train_x, train_y):

    '''
    This function will preprocess kickstarter text
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