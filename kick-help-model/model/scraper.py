import os
import csv
import re
import requests
import json

#data_folder = os.path.join(os.getcwd(), '')
data_folder = os.path.join(os.pardir, 'data')
dataset1_path = os.path.join(data_folder, 'ks-projects-201612.csv')
dataset2_path = os.path.join(data_folder, 'ks-projects-201801.csv')

def scrape_from_csv(dataset_path):
    # this will search for every path
    with open(dataset_path, 'r') as csvfile:
        dataset1 = csv.reader(csvfile)
        for counter, row in enumerate(dataset1):
            if counter == 0:
                continue
            name = row[1]
            name_pattern = re.compile(name)
            search = requests.get('http://www.kickstarter.com/projects/search.json?search=&term={}'.format(name))
            search_response = search.json()
            for project in search_response['projects']:
                if name_pattern.match(project['name']):
                    # navigate into project and get description, blurb, etc.
                    project_url = project['urls']['web']['project']
                    scrape_from_url(project_url)
                    print(project_url)


def scrape_from_url(project_url):
    '''
    #############
    YOU GON' NEED INSTALL REQUESTS BOI
    pip install requests
    ##########
    :return:
    '''
    # blurb is here div class="NS_project_profiles__blurb"
    # description is here: div id="full-description"
    r = requests.get(project_url)
    # get text of html
    r = project_url.text


if __name__ == '__main__':
    scrape_from_csv(dataset_path=dataset1_path)


'''
how to pretty print json:
print(json.dumps(<JSON_DATA>, indent=2))
'''