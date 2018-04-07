#import keras
import numpy as np
import os
import sys
sys.path.append('C:\\Users\\lewys\\PycharmProjects\\kick-help\\kick_help_api\\')
import scrape
import keras

data_folder = os.path.join(os.pardir, 'data')
dataset1_path = os.path.join(data_folder, 'ks-projects-201612.csv')
dataset2_path = os.path.join(data_folder, 'ks-projects-201801.csv')



def train(train_x, train_y):
    return


def preprocess(text):
    return



if __name__ == '__main__':
    # train_x, train_y = scrape_from_csv(dataset_path=dataset1_path)
    # print("Data: {}\nLabels: {}".format(train_x, train_y))
    num_classes = 2
    raw_train_data, raw_train_labels = scrape.scrape_from_csv(dataset1_path)

    features = np.empty((0, 50), dtype='float32')
    labels = np.empty(0, dtype=np.int)
    for project in raw_train_data:
        #description_values = (wm.get_word_values((project['description']), word_model))
        for param in raw_train_data:
            print(param)

    train_x = np.array(features)
    train_y = []
    #train_y = keras.utils.to_categorical(raw_train_labels, num_classes)
    train(train_x, train_y)