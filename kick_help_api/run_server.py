import flask
from flask import request
from flask_cors import CORS
import scrape
import kick_help_model.model.model_simple as ms

app = flask.Flask(__name__)
CORS(app)
model_simple = None


def load_model():
	# get global models
	global model_simple
	# load luis' model


@app.route('/predict', methods = ['GET', 'POST'])
def predict():
	# get global models
	global model_simple
	# get data
	scrape_results = scrape.scrape_from_url(request.args['url'])
	data = {'success': 0.74}
	# predict
	return flask.jsonify(data)


if __name__ == '__main__':
	print(('* loading keras model and flask starting server...'
		'please wait until server has fully started'))
	load_model()
	app.run()