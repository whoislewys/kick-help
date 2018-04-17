import csv
from datetime import datetime


RAW_PROJECT_COUNT = 0
CLEAN_PROJECT_COUNT = 0
CLEAN_SUCCESSFUL_COUNT = 0
CLEAN_FAILED_COUNT = 0
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


def clean(infile, outfile):
	# read from csv
	print('Cleaning Project List...')
	with open(infile, 'r', encoding='latin-1') as csvfile:
		reader = csv.DictReader(csvfile)
		data = [r for r in reader]
		X = []
		# clean
		for p in data:
			try:
				name = p['name'].lower()
				category = p['category'].lower()
				duration = get_duration(p['launched'], p['deadline'])
				goal = p['goal']
				outcome = p['state']
				if outcome == 'successful' and category in CATEGORIES:
					new_p = make_project(name, category, duration, goal, 1)
					X.append(new_p)
				elif outcome == 'failed' and category in CATEGORIES:
					new_p = make_project(name, category, duration, goal, 0)
					X.append(new_p)
			except:
				pass
	# write to csv
	print('Writing Clean List...')
	with open(outfile, 'w', encoding='latin-1') as csvfile:
		keys = list(X[0].keys())
		writer = csv.DictWriter(csvfile, fieldnames=keys, lineterminator='\n')
		writer.writeheader()
		for p in X:
			writer.writerow(p)
		
	# summary
	RAW_PROJECT_COUNT = len(data)
	CLEAN_PROJECT_COUNT = len(X)
	CLEAN_SUCCESSFUL_COUNT = sum(p['outcome'] == 1 for p in X)
	CLEAN_FAILED_COUNT = sum(p['outcome'] == 0 for p in X)
	print('Raw Project Count:', RAW_PROJECT_COUNT)
	print('Clean Project Count:', CLEAN_PROJECT_COUNT)
	print('Clean Succesful Count:', CLEAN_SUCCESSFUL_COUNT)
	print('Clean Failed Count:', CLEAN_FAILED_COUNT)


def get_duration(launched, deadline):
    t1 = datetime.strptime(launched[0:18], '%Y-%m-%d %H:%M:%S')
    t2 = datetime.strptime(deadline[0:18], '%Y-%m-%d %H:%M:%S')
    t3 = t2 - t1
    return(str(t3.total_seconds()))


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


if __name__ == '__main__':
	print('Project List 1:')
	clean('raw-projects-1.csv', 'clean-projects-1.csv')