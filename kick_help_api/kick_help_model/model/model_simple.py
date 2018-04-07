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

data_folder = os.path.join(os.pardir, 'data')
dataset1_path = os.path.join(data_folder, 'ks-projects-201612.csv')
dataset2_path = os.path.join(data_folder, 'ks-projects-201801.csv')


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


def train(train_x, train_y):
    input_dim = len(train_x[0])
    model = Sequential()
    model.add(Dense(500, input_dim=input_dim))
    model.add(Activation('relu'))
    model.add(Dropout(0.4))
    model.add(Dense(300))
    model.add(Activation('relu'))
    model.add(Dropout(0.4))
    model.add(Dense(10))
    model.add(Activation('softmax'))
    return


def preprocess(text):
    return


if __name__ == '__main__':
    # train_x, train_y = scrape_from_csv(dataset_path=dataset1_path)
    # print("Data: {}\nLabels: {}".format(train_x, train_y))
    num_classes = 2
    raw_train_data, raw_train_labels = scrape.scrape_from_csv(dataset1_path)

    features = []
    #features = np.empty((0, 50), dtype='float32')
    labels = np.empty(0, dtype=np.int)
    for project in raw_train_data:
        #description_values = (wm.get_word_values((project['description']), word_model))
        for param in raw_train_data:
            proj_category = np.float32(category_to_int(cat=param['category']))
            print('proj category: ', proj_category)
            proj_goal = param['goal']
            proj_duration = param['duration']
            proj_raised = param['raised']
            features.append(proj_goal)
            features.append(proj_duration)
            features.append(proj_raised)
            print(features)
            project_category = category_to_int(cat=param['category']).astype(np.float32)
            features.append(param['category'])
            # category (cast to int)
            # goal
            # duration float seconds
            # label = raised

    train_x = np.array(features)
    train_y = []
    train_y = keras.utils.to_categorical(raw_train_labels, num_classes)
    train(train_x, train_y)