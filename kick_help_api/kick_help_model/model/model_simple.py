#import keras
import numpy as np
import os
import sys
# TODO: make this actually compatible
sys.path.append('C:\\Users\\lewys\\PycharmProjects\\kick-help\\kick_help_api\\')
import scrape
import tensorflow as tf
import keras
from keras import Model
from sklearn.preprocessing import LabelEncoder
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras import backend as K
import h5py

data_folder = os.path.join(os.pardir, 'data')
TRAIN_DATA_PATH = os.path.join(data_folder, 'ks-projects-train.csv')
TEST_DATA_PATH = os.path.join(data_folder, 'ks-projects-test.csv')


def category_to_int(cat):
    cat_enum = ['games',
                'design',
                'technology',
                'film & video',
                'music',
                'fashion',
                'publishing',
                'food',
                'art',
                'comics',
                'theater',
                'photography',
                'crafts',
                'dance',
                'journalism']
    try:
        var = cat_enum.index(cat)
    except:
        var = 1
    return var


def load_data(csv_path):
    raw_train_data, y_train = scrape.scrape_from_csv(csv_path)
    v_stack_features = np.empty((0, 3), dtype='float32')
    for project in raw_train_data:
        proj_category = np.float32(category_to_int(project['category']))
        try:
            proj_goal = np.float32(project['goal'])
        except Exception as e:
            proj_goal = np.float32(1000)
        proj_duration = np.float32(project['duration'])
        features = [proj_goal, proj_duration, proj_category]
        h_stack_features = np.hstack(features)
        v_stack_features = np.vstack([v_stack_features, h_stack_features])

    x_train = np.array(v_stack_features)
    #y_train = keras.utils.to_categorical(raw_train_labels, num_classes)
    return x_train, np.array(y_train)


def train(x_train, y_train, x_test, y_test):
    batch_size = 25
    epochs = 3
    lr = 0.001
    input_dim = (x_train.shape[1])
    model = Sequential()
    model.add(Dense(20, input_dim=input_dim, activation='sigmoid'))
    model.add(Dense(1, activation='sigmoid'))

    opt = keras.optimizers.rmsprop(lr=lr)
    model.compile(optimizer=opt, loss='binary_crossentropy', metrics=['binary_accuracy'])
    model.fit(x=x_train, y=y_train,
              batch_size=batch_size,
              epochs=epochs,
              verbose=1,
              )
    model.save('kick_help_model_simple_3.h5')
    return


def predict():
    # 1 in the first column is success
    # 1 in the second column is failure
    model = keras.models.load_model('kick_help_model_simple_3.h5')
    # x should be in format goal, duration, category
    X = np.array([8000, 2592000, 11], dtype='float32')
    # print(X)
    X.shape = (1, len(X))
    prediction = model.predict(X)
    print('Prediction: ', prediction)
    print('Pred type: ', type(prediction))


def inspect_weights():
    # 1 in the first column is success
    # 1 in the second column is failure
    X = np.array([1000, 5000000, 7], dtype='float32')
    X.shape = (1, len(X))
    model = keras.models.load_model('kick_help_model_simple_2.h5')
    get_1st_layer_op = K.function([model.layers[0].input, K.learning_phase()], [model.layers[0].output])
    layer_output = get_1st_layer_op([X,0])[0]
    # sigmoid(wx+b)
    prediction = (sum(layer_output))
    #prediction = model.predict(X)
    print(prediction)
    print(type(prediction))


if __name__ == '__main__':
    print('Loading training data...')
    x_train, y_train = load_data(csv_path=TRAIN_DATA_PATH)
    # x_train = [n/x_train.max() for n in x_train]
    # x_train = np.asarray(x_train)
    # y_train = np.asarray(y_train)
    #x_train = np.random.random((80000, 3))
    #y_train = np.random.randint(2, size=(80000, 1))
    print('Loading testing data...')
    x_test, y_test = load_data(csv_path=TEST_DATA_PATH)
    # x_test = [n / x_test.max() for n in x_test]
    # x_test = np.asarray(x_test)
    #y_test = np.asarray(y_test)
    #x_test = np.random.random((2000, 3))
    #y_test = np.random.randint(2, size=(2000, 1))
    print('train data dimensionality: ', x_train.shape)
    print('test data dimensionality: ', x_test.shape)
    train(x_train, y_train, x_test, y_test)
    predict()
    #inspect_weights()
