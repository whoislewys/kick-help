#import keras
import numpy as np
import os
import sys
# TODO: make this actually compatible
sys.path.append('C:\\Users\\lewys\\PycharmProjects\\kick-help\\kick_help_api\\')
import scrape
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
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
        var = -1
    return var


def load_data(csv_path):
    raw_train_data, raw_train_labels = scrape.scrape_from_csv(csv_path)
    num_classes = 2
    features = []
    v_stack_features = np.empty((0, 3), dtype='float32')
    labels = np.empty(0, dtype=np.int)

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
    y_train = keras.utils.to_categorical(raw_train_labels, num_classes)
    return x_train, y_train


def train(x_train, y_train, x_test , y_test):
    num_classes = 2
    batch_size = 250
    epochs = 20
    lr = 0.01
    input_dim = (x_train.shape[1])
    model = Sequential()
    model.add(Dense(150, input_dim=input_dim, activation='relu'))
    model.add(Dropout(0.4))
    model.add(Dense(50, activation='relu'))
    model.add(Dropout(0.4))
    model.add(Dense(num_classes, activation='softmax'))

    sgd = keras.optimizers.SGD(lr=lr, momentum=0.9, nesterov=True)
    model.compile(optimizer=sgd, loss='binary_crossentropy', metrics=['binary_accuracy'])
    model.fit(x=x_train, y=y_train,
              batch_size=batch_size,
              epochs=epochs,
              verbose=1,
              validation_data=(x_test, y_test),
              shuffle=True)
    model.save('kick_help_model_simple.h5')
    return


def predict():
    model = keras.models.load_model('kick_help_model_simple_sig.h5')
    # x should be in format goal, duration, category
    X = np.array([1000, 4095420, 7], dtype='float32')
    X.shape = (1, len(X))
    prediction = model.predict(X)
    print(prediction)


if __name__ == '__main__':

    # print("Data: {}\nLabels: {}".format(x_train, y_train))
    num_classes = 2
    print('Loading training data...')
    x_train, y_train = load_data(csv_path=TRAIN_DATA_PATH)
    print('Loading testing data...')
    x_test, y_test = load_data(csv_path=TEST_DATA_PATH)

    print('train data dimensionality: ', x_train.shape)
    print('train label dimensionality: ', y_train.shape)
    print('test data dimensionality: ', x_test.shape)
    print('test label dimensionality: ', y_test.shape)
    train(x_train, y_train, x_test, y_test)

    predict()
