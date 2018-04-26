import csv
import numpy as np
import os
import keras
from keras import Model
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras import backend as K
import h5py

# constants
DATA_PATH = os.path.join(os.pardir, 'data', 'clean-projects-1.csv')

# load data
def load_data(infile):
	x_train = []
	y_train = []
	# load
	with open(infile, 'r', encoding='latin-1') as csvfile:
		reader = csv.DictReader(csvfile)
		data = [r for r in reader]
	v_stack = np.empty((0, 3), dtype='float32')
	# format
	for p in data:
		category = np.float32(p['category'])
		duration = np.float32(p['duration'])
		goal = np.float32(p['goal'])
		features = [category, duration, goal]
		h_stack = np.hstack(features)
		v_stack = np.vstack([v_stack, h_stack])
		y_train.append(p['outcome'])
	x_train = np.array(v_stack)
	y_train = np.array(y_train)
	return x_train, y_train

# scale x's
def scale(x_train):
	category_max = x_train[:,0].max()
	duration_max = x_train[:,1].max()
	goal_max = x_train[:,2].max()
	x_train[:,0] = [n / category_max for n in x_train[:,0]]
	x_train[:,1] = [n / duration_max for n in x_train[:,1]]
	x_train[:,2] = [n / goal_max for n in x_train[:,2]]
	print('category_max:', category_max)
	print('duration_max:', duration_max)
	print('goal_max:', goal_max)
	return x_train

# train keras model
def model_train(x_train, y_train, batch_size, epochs, lr, nodes, save):
	batch_size = batch_size
	epochs = epochs
	lr = lr
	input_dim = (x_train.shape[1])
	model = Sequential()
	model.add(Dense(nodes, input_dim=input_dim, activation='sigmoid'))
	model.add(Dense(1, activation='sigmoid'))
	opt = keras.optimizers.rmsprop(lr=lr)
	model.compile(optimizer=opt, loss='binary_crossentropy', metrics=['binary_accuracy'])
	metrics = model.fit(x=x_train, y=y_train,
			batch_size=batch_size,
			epochs=epochs,
			verbose=1,
			)
	if save == 1:
		model.save('model.h5')
	return metrics.history['binary_accuracy'][0]

# find optimal parameters
def model_validate(x_train, y_train):
	# options
	batch_size = 50
	epochs = 1000
	lr = 0.05 # [0.01, 0.02, ... 0.1]
	nodes = np.arange(1, 102, 10) # [1, 3, ... 100]
	x = []
	# validate
	for i in nodes:
		print("Model With", i, "Nodes...")
		accuracy = model_train(x_train, y_train, batch_size, epochs, lr, i, 0)
		x.append(accuracy)
	# save accuracy
	np.savetxt('model_accuracy.txt', x, fmt='%f') # [1, 11, ... 101]
	return x

# run
if __name__ == '__main__':
	# find optimal nodes
	x_train, y_train = load_data(DATA_PATH)
	x_train = scale(x_train)
	accuracy = model_validate(x_train, y_train)
	max_accuracy = max(accuracy)
	opt_nodes = accuracy.index(max_accuracy) * 10 + 1
	print('Optimal Nodes:', opt_nodes)
	# create model with optimal nodes
	accuracy = model_train(x_train, y_train, 50, 10000, 0.05, opt_nodes, 1) # optimal nodes = 11
	print('Model Accuracy:', accuracy)