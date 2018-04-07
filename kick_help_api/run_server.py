import numpy as np
import flask
import io
import os
import scrape
import sys
from kick_help_model.model.word_model import word_model as wm


app = flask.Flask(__name__)
model = None

def load_model():
	global model
	global word_model
	# define model
	word_model = wm.load_word_model()

@app.route('/predict', methods = ['GET', 'POST'])
def predict():
	url = request.data


	return flask.jsonify(data)

if __name__ == '__main__':
	print(('* loading keras model and flask starting server...'
		'please wait until server has fully started'))
	load_model()
	app.run()