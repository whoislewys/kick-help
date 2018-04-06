import pandas as pd
import numpy as np
import os
import csv

#data_folder = os.path.join(os.getcwd(), '')
dataset1_path = r'C:\Users\lewys\PycharmProjects\kick-help\data\ks-projects-201612.csv'

#dataset1 = pd.read_csv(dataset1_path)
with open(dataset1_path, 'r') as csvfile:
    #dataset1 = pd.read_csv(dataset1_path)
    dataset1 = csv.reader(csvfile)
    for row in dataset1:
        print(', '.join(row))

#print(type(dataset1))