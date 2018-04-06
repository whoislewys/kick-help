import pandas as pd
import numpy as np
import os
import csv

#data_folder = os.path.join(os.getcwd(), '')
data_folder = os.path.join(os.pardir, 'data')
print(data_folder)
dataset1_path = os.path.join(data_folder, 'ks-projects-201612.csv')
dataset2_path = os.path.join(data_folder, 'ks-projects-201801.csv')

with open(dataset1_path, 'r') as csvfile:
    #dataset1 = pd.read_csv(dataset1_path)
    dataset1 = csv.reader(csvfile)
    for row in dataset1:
        row = row
        # print(', '.join(row))

