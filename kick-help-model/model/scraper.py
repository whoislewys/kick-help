import os
import csv
import re
import requests
import json
from lxml import html
from datetime import datetime

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
            elif counter == 4:
                break
            name = row[1]
            name_pattern = re.compile(name)
            search = requests.get('http://www.kickstarter.com/projects/search.json?search=&term={}'.format(name))
            search_response = search.json()
            for project in search_response['projects']:
                if name_pattern.match(project['name']):
                    project_url = project['urls']['web']['project']
                    scrape_from_url(project_url)


def scrape_from_url(project_url):
    # init dictionary
    data = {'category': '',
            'blurb': '',
            'title': '',
            'duration': '',
            'goal': '',
            'description': '',
            'risks': '',
            'biography': '',
            'name': ''}

    # get html tree
    page = requests.get(project_url)
    tree = html.fromstring(page.content)

    # get content
    data['category'] = tree.xpath('//a[@class="nowrap navy-700 flex items-center medium mr3 type-12"]/text()')[0]
    data['title'] = tree.xpath('//div[@class="col-20-24 col-lg-15-24 hide block-md order-2-md"]//h2/text()')[0]
    data['blurb'] = tree.xpath('//div[@class="col-20-24 col-lg-15-24 hide block-md order-2-md"]//p/text()')[0]
    
    
    time1 = tree.xpath('//div[@class="NS_campaigns__funding_period"]//p//time[1]/@datetime')[0]
    time2 = tree.xpath('//div[@class="NS_campaigns__funding_period"]//p//time[2]/@datetime')[0]
    data['duration'] = get_duration(time1, time2)

    # clean
    for key in data:
        data[key] = data[key].replace('\n', ' ').strip()
        print(data[key])

def get_duration(time1, time2):
    # year, month, day, hour=0, minute=0, second=0, microsecond=0,
    t1 = datetime.strptime(time1[0:18], '%Y-%m-%dT%H:%M:%S')
    t2 = datetime.strptime(time2[0:18], '%Y-%m-%dT%H:%M:%S')
    t3 = t2 - t1
    return(str(t3.total_seconds()))

if __name__ == '__main__':
    scrape_from_csv(dataset_path=dataset1_path)


'''
how to pretty print json:
print(json.dumps(<JSON_DATA>, indent=2))
'''