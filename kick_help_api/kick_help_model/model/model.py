#################################################
#               UNMODIFIED                      #
#################################################


import numpy
import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# define categories
CATEGORIES = set(['games',
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
            'journalism'])

# set random seed
seed = 7
numpy.random.seed(seed)

# load data
'''
dataframe = pandas.read_csv('sonar.csv', header=None)
dataset = dataframe.values
'''
dataframe = pandas.read_csv('ks-projects-201612.csv', encoding='latin-1')
dataset = dataframe[:, 0:13]
print(dataset)
# format data
X = dataset[:,0:60].astype(float) # (208, 60)
Y = dataset[:,60] # (208,)

# format labels
encoder = LabelEncoder()
encoder.fit(Y)
encoded_Y = encoder.transform(Y) # (208,)

# baseline model
def create_baseline():
	model = Sequential()
	model.add(Dense(60, input_dim=60, kernel_initializer='normal', activation='relu'))
	model.add(Dense(1, kernel_initializer='normal', activation='sigmoid'))

	model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model

# train and test
'''
estimator = KerasClassifier(build_fn=create_baseline, epochs=100, batch_size=5, verbose=0)
kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=seed)
results = cross_val_score(estimator, X, encoded_Y, cv=kfold)
print('results: %.2f%% (%.2f%%)' % (results.mean()*100, results.std()*100))
'''