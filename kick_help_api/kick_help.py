import os
import keras
import numpy as np
import requests
import json
import kick_help_model.data.clean as c

CATEGORY_MAX = 14
DURATION_MAX = 7948800
GOAL_MAX = 100000000

MODEL_PATH = os.path.join('kick_help_model', 'model', 'model.h5')

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
		data['category'] = c.get_category(project['category']['slug'].split('/')[0])
		data['duration'] = np.float32(project['deadline'] - project['launched_at'])
		data['goal'] = np.float32(project['goal'])
		return data 

def predict(title):
	model = keras.models.load_model(MODEL_PATH)
	data = get_page(url)
	if data == -1:
		print('\nProject Could Not Be Found')
	else:
		category = data['category']
		duration = data['duration']
		goal = data['goal']
		x = np.array([category/CATEGORY_MAX, duration/DURATION_MAX, goal/GOAL_MAX])
		x.shape = (1, len(x))
		result = float(model.predict(x))
		print('\nProbability of Success For', data['name'],':', result)

if __name__ == '__main__':
	url = input('\nEnter Project Title: ').lower()
	print('Predicting...\n')
	predict(url)
