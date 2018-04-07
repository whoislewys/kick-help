from flask import request
import flask
import scrape
import pandas as pd

app = flask.Flask(__name__)
model = None
word_model = None


def load_model():
	# get global models
	global model


@app.route('/predict', methods = ['GET', 'POST'])
def predict():
	# get global models
	global model
	# predict
	url = request.data
	return flask.jsonify('test string')


if __name__ == '__main__':
	print(('* loading keras model and flask starting server...'
		'please wait until server has fully started'))
	load_model()
	app.run()