import os
import csv
import re
import requests
import json
from lxml import html
from datetime import datetime

# data_folder = os.path.join(os.getcwd(), '')
data_folder = os.path.join(os.pardir, 'data')
dataset1_path = os.path.join(data_folder, 'ks-projects-201612.csv')
dataset2_path = os.path.join(data_folder, 'ks-projects-201801.csv')

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


def scrape_from_csv(dataset_path):
    # 64 per second
    # open data
    X = []
    Y = []
    with open(dataset_path, 'r') as csvfile:
        # TODO validate title - remove quotes and parenthesis
        dataset1 = csv.reader(csvfile)
        # iterate through projects
        for counter, row in enumerate(dataset1):
            # give everything default values
            try:
                outcome = row[9]  # possible values: success, failed, canceled (sic)
            except:
                outcome = '0'

            try:
                category = row[3].lower()
            except:
                category = 'food'

            try:
                goal = row[6]
            except:
                goal = '1000'

            deadline = row[5]
            launched = row[7]
            name = row[1]

            # print('cat before checking: ', category)
            #if counter == 0 or outcome == 'canceled' or outcome == 'suspended': # ignore csv categories and canceled projects
            if counter == 0 or (outcome != 'successful' and outcome != 'failed'):
                continue
            elif category not in CATEGORIES:
                continue
            elif '(' in name or ')' in name:
                continue
            elif counter >= 100000:
                break

            try:
                duration = get_duration(launched, deadline)
            except:
                duration = '0'

            # print('scraping: {}, number: {}'.format(name, counter))
            scrape_results = scrape_for_training( category, goal, duration)
            X.append(scrape_results)
            num_label = label_to_number(outcome)
            #num_label = outcome
            Y.append((num_label,))
    return X, Y


def scrape_for_training(category, goal, duration):
    # TODO update this to better match error checking done in funct above
    # init dictionary
    data = {'category': '',
            'blurb': '',
            'title': '',
            'duration': '',
            'goal': '',
            'raised': '',
            'description': '',
            'risks': '',
            'name': ''}
    data['category'] = category
    data['goal'] = goal
    data['duration'] = duration
    # clean
    for key in data:
        data[key] = data[key].replace('\n', ' ').strip()

    return data


def scrape_from_url(project_url):
    # TODO update this to better match error checking done in funct above
    # init dictionary
    data = {'category': '',
            'blurb': '',
            'title': '',
            'duration': '',
            'goal': '',
            'raised': '',
            'description': '',
            'risks': '',
            'name': ''}
    # get html tree
    page = requests.get('https://www.kickstarter.com/projects/search.json?search=&tearm={}'.format(project_url.split('/')[-1]))
    response = page.json()
    project = response['projects'][0] 

    data['category'] = project['category']['slug'].split('/')[0]
    data['goal'] = project['goal']
    data['duration'] = project['deadline'] - project['launched_at']   

    # return
    return data


def label_to_number(outcome): # text_label is success=0, failed=1, canceled=2 (sic)
    if outcome == 'successful':
        num_label = 0
    elif outcome == 'failed':
        num_label = 1
    else:
        num_label = 0
    return num_label


def get_duration(launched, deadline):
    # convert string to datetime
    t1 = datetime.strptime(launched[0:18], '%Y-%m-%d %H:%M:%S')
    t2 = datetime.strptime(deadline[0:18], '%Y-%m-%d %H:%M:%S')
    # get delta
    t3 = t2 - t1
    # return
    return(str(t3.total_seconds()))

def get_duration_url(launched, deadline):
    # convert string to datetime
    t1 = datetime.strptime(launched[0:18], '%Y-%m-%dT%H:%M:%S')
    t2 = datetime.strptime(deadline[0:18], '%Y-%m-%dT%H:%M:%S')
    # get delta
    t3 = t2 - t1
    # return
    return(str(t3.total_seconds()))


if __name__=='__main__':
    print('yup')
    #
    # FOR TESTING
    # TRAIN_DATA_PATH = r'C:\Users\lewys\PycharmProjects\kick-help\kick_help_api\kick_help_model\data\ks-projects-train.csv'
    # raw_train_data, raw_train_labels = scrape_from_csv(TRAIN_DATA_PATH)
    # print(len(raw_train_data), len(raw_train_labels))
    # print()
    #