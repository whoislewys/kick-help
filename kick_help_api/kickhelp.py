import csv
from datetime import datetime
import os
import keras
from keras import Model
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
import h5py
import numpy as np
import requests
import json

CATEGORY_MAX = 14 # taken from previous run on data
DURATION_MAX = 7948800 # taken from previous run on data
GOAL_MAX = 100000000 # taken from previous run on data
CATEGORIES = ['games',
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

#####################################
#		   CLEAN FUNCTIONS          #
#####################################

# clean data set
def clean(infile, outfile):
	# init
	raw_project_count = 0
	clean_project_count = 0
	clean_successful_count = 0
	clean_failed_count = 0
	# read from csv
	print('Cleaning Project List...')
	with open(infile, 'r', encoding='latin-1') as csvfile:
		reader = csv.DictReader(csvfile)
		data = [r for r in reader]
		x = []
		# clean
		for p in data:
			try:
				name = p['name'].lower()
				category = p['category'].lower()
				duration = get_duration(p['launched'], p['deadline'])
				goal = p['goal']
				outcome = p['state']
				if outcome == 'successful' and category in CATEGORIES:
					category = get_category(category)
					new_p = make_project(name, category, duration, goal, 1)
					x.append(new_p)
				elif outcome == 'failed' and category in CATEGORIES:
					category = get_category(category)
					new_p = make_project(name, category, duration, goal, 0)
					x.append(new_p)
			except:
				pass
	# write to csv
	print('Writing Clean List...')
	with open(outfile, 'w', encoding='latin-1') as csvfile:
		keys = list(x[0].keys())
		writer = csv.DictWriter(csvfile, fieldnames=keys, lineterminator='\n')
		writer.writeheader()
		for p in x:
			writer.writerow(p)	
	# summary
	raw_project_count = len(data)
	clean_project_count = len(x)
	clean_successful_count = sum(p['outcome'] == 1 for p in x)
	clean_failed_count = sum(p['outcome'] == 0 for p in x)
	print('Raw Project Count:', raw_project_count)
	print('Clean Project Count:', clean_project_count)
	print('Clean Succesful Count:', clean_successful_count)
	print('Clean Failed Count:', clean_failed_count)

# category to num
def  get_category(category):
	return CATEGORIES.index(category)

# datetime to num
def get_duration(launched, deadline):
    t1 = datetime.strptime(launched[0:18], '%Y-%m-%d %H:%M:%S')
    t2 = datetime.strptime(deadline[0:18], '%Y-%m-%d %H:%M:%S')
    t3 = t2 - t1
    return(str(t3.total_seconds()))

# project structure
def make_project(name, category, duration, goal, outcome):
	data = {'name': '',
			'category': '',
			'duration': '',
			'goal': '',
			'outcome': ''}
	data['category'] = category
	data['duration'] = duration
	data['goal'] = goal
	data['name'] = name
	data['outcome'] = outcome
	return data

#####################################
#		   TRAIN FUNCTIONS          #
#####################################

# load data from clean
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
	return x_train

# train keras model
def model_train(x_train, y_train, batch_size, epochs, lr, nodes, save, outfile='model.h5'):
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
		model.save(outfile)
	return metrics.history['binary_accuracy'][0]

# find optimal parameters
def model_validate(x_train, y_train, batch_size, epochs, lr, min_nodes, max_nodes, step, outfile='model_accuracy.txt'):
	# options
	batch_size = batch_size # 50
	epochs = epochs # 1000
	lr = lr # 0.05
	nodes = np.arange(min_nodes, max_nodes, step) # [1, 11, ... 101]
	x = []
	# validate
	for i in nodes:
		print("Model With", i, "Nodes...")
		accuracy = model_train(x_train, y_train, batch_size, epochs, lr, i, 0)
		x.append(accuracy)
	# save accuracy
	np.savetxt(outfile, x, fmt='%f')

	max_accuracy = max(x)
	opt_nodes = x.index(max_accuracy) * step + min_nodes
	return opt_nodes, max_accuracy

#####################################
#		 PREDICT FUNCTIONS          #
#####################################

# scrape kickstarter
def get_page(title):
	data = {'name': '',
			'category': '',
			'duration': '',
			'goal': ''}
	request_string = 'https://www.kickstarter.com/projects/search.json?search=&term={}'.format('-'.join(title.split(' ')))
	page = requests.get(request_string)
	response = page.json()
	if response['total_hits'] == 0:
		return -1
	else:
		project = response['projects'][0]
		data['name'] = project['name']
		data['category'] = get_category(project['category']['slug'].split('/')[0])
		data['duration'] = np.float32(project['deadline'] - project['launched_at'])
		data['goal'] = np.float32(project['goal'])
		return data 

# predict success
def predict(title, model='model.h5'):
	model = keras.models.load_model(model)
	data = get_page(title)
	if data == -1:
		print('Project Could Not Be Found')
	else:
		category = data['category']
		duration = data['duration']
		goal = data['goal']
		x = np.array([category/CATEGORY_MAX, duration/DURATION_MAX, goal/GOAL_MAX])
		x.shape = (1, len(x))
		result = float(model.predict(x))
		print('Probability of Success For', data['name'],':', result)

if __name__ == '__main__':
	# test clean functions
	#print()
	#clean('raw_projects_1.csv', 'clean_projects_1.csv')

	# test model functions
	#print()
	#batch_size = 50
	#epochs = 1
	#lr = 0.05
	#min_nodes = 1
	#max_nodes = 3
	#step = 1
	#x_train, y_train = load_data('clean_projects_1.csv')
	#x_train = scale(x_train)
	#opt_nodes, accuracy = model_validate(x_train, y_train, batch_size, epochs, lr, min_nodes, max_nodes, step, 'test_accuracy.txt')
	#model_train(x_train, y_train, batch_size, epochs, lr, opt_nodes, 1, 'test_model.h5')

	# test predict functions
	print()
	url = input('Enter Project Title: ').lower()
	print('Predicting...\n')
	predict(url)