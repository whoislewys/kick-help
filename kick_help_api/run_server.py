import flask
from flask import request
from flask_cors import CORS
import os
import scrape
import keras
import h5py
import numpy as np
from kick_help_model.model.model_simple import category_to_int

app = flask.Flask(__name__)
CORS(app)
model = None


def load_model():
	# get global models
	global model
	model = keras.models.load_model(os.path.join(os.getcwd(), 'kick_help_model', 'model', 'kick_help_model_simple.h5'))
	# load luis' model


@app.route('/predict', methods = ['GET', 'POST'])
def predict():
	# get global models
	global model
	# get data
	'''results = scrape.scrape_from_url(request.args['url'])
	goal = np.float32(results['goal'])
	duration = np.float32(results['duration'])
	category = np.float32(category_to_int(results['category']))
	x = np.array([goal, duration, category], dtype='float32')
	x.shape = (1, x.shape[0])
	data = {'success': int(model.predict(x)[0][0])}'''
	# predict
	data = {'success': request.args['num']}
	return flask.jsonify(data)


if __name__ == '__main__':
	print(('* loading keras model and flask starting server...'
		'please wait until server has fully started'))
	load_model()
	app.run()