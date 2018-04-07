from flask import request
import flask
import scrape
from kick_help_model.model import word_model as wm
import pandas as pd

app = flask.Flask(__name__)
model = None
word_model = none


def load_model():
	# get global models
	global model
	global word_model
	# define model
	word_model = wm.load_word_model()


@app.route('/predict', methods = ['GET', 'POST'])
def predict():
	# get global models
	global model
	global word_model
	# predict
	url = request.data
	data = wm.get_word_values('hello', word_model)
	print(data)
	return flask.jsonify('test string')


if __name__ == '__main__':
	print(('* loading keras model and flask starting server...'
		'please wait until server has fully started'))
	load_model()
	app.run()