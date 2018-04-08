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
    v_stack_features = np.empty((0, 4), dtype='float32')
    labels = np.empty(0, dtype=np.int)
    for project in raw_train_data:
        #description_values = (wm.get_word_values((project['description']), word_model))
        for param in raw_train_data:
            proj_category = np.float32(category_to_int(cat=param['category']))
            if proj_category == -1:
                continue
            proj_goal = np.float32(param['goal'])
            proj_duration = np.float32(param['duration'])
            proj_raised = np.float32(param['raised'])
            features = [proj_goal, proj_duration, proj_raised, proj_category]
            # features.append(proj_goal)
            # features.append(proj_duration)
            # features.append(proj_raised)
            # features.append(proj_category)
            h_stack_features = np.hstack(features)
            v_stack_features = np.vstack([v_stack_features, h_stack_features])
            # category (cast to int)
            # goal
            # duration float seconds
            # label = raised

    train_x = np.array(v_stack_features)

    train_y = keras.utils.to_categorical(raw_train_labels, num_classes)
    print(train_x)
    print(train_y)
    train(train_x, train_y)
