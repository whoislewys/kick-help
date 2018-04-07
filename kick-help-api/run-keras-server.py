import numpy as np
import flask
import io

app = flask.Flask(__name__)
model = None

def load_model():
	global model
	# define model

@app.route('/predict', methods = ['GET', 'POST'])
def predict():
	data = {'status': 'Null'}
	data['status'] = flask.request.method

	return flask.jsonify(data)

if __name__ == '__main__':
	print(('* loading keras model and flask starting server...'
		'please wait until server has fully started'))
	load_model()
	app.run()