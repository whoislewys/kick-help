import flask
from flask import request
from flask_cors import CORS
import os
import scrape
import keras
import h5py
import numpy as np
from kick_help_model.model import *
from kick_help_model.model.model_simple import category_to_int

app = flask.Flask(__name__)
CORS(app)


@app.route('/predict', methods = ['GET', 'POST'])
def predict():
	# get data
	model = keras.models.load_model('kick_help_model_simple_3.h5')
	page = scrape.scrape_from_url(request.args['url'])
	goal = np.float32(page['goal'])
	duration = np.float32(page['duration'])
	category = np.float32(category_to_int(page['category']))
	x = np.array([goal, duration, category], dtype='float32')
	x.shape = (1, len(x))
	results = model.predict(x)
	data = {'success': float(results)}
	return flask.jsonify(data)


if __name__ == '__main__':
	app.run()