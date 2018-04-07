import os
import csv
import re
import requests
import json

#data_folder = os.path.join(os.getcwd(), '')
data_folder = os.path.join(os.pardir, 'data')
dataset1_path = os.path.join(data_folder, 'ks-projects-201612.csv')
dataset2_path = os.path.join(data_folder, 'ks-projects-201801.csv')

# this will search for every path
with open(dataset1_path, 'r') as csvfile:
    dataset1 = csv.reader(csvfile)
    for counter, row in enumerate(dataset1):
        if counter == 0:
            continue
        name = row[1]
        name_pattern = re.compile(name)
        # r = requests.get('https://www.kickstarter.com/discover/advanced?category_id=1&ref=nav_search&term={}'.format(name))
        search = requests.get('http://www.kickstarter.com/projects/search.json?search=&term={}'.format(name))
        search_response = search.json()
        for project in search_response['projects']:
            if name_pattern.match(project['name']):
                # navigate into project and get description, blurb, etc.
                project_url = project['urls']['web']['project']
                blurb = project['blurb']

                print(project_url)


'''
how to pretty print json:
print(json.dumps(<JSON_DATA>, indent=2))
'''