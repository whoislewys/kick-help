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


def scrape_from_csv(dataset_path):
    # open data
    X = []
    Y = []
    with open(dataset_path, 'r') as csvfile:
        dataset1 = csv.reader(csvfile)
        # iterate through projects
        for counter, row in enumerate(dataset1):
            text_label = row[9]  # possible values: success, failed, canceled (sic)
            if counter == 0 or text_label == 'canceled': # ignore csv categories and canceled projects
                continue
            elif counter == 10:
                break
            name = row[1]
            name_pattern = re.compile(name)
            search = requests.get('http://www.kickstarter.com/projects/search.json?search=&term={}'.format(name))
            search_response = search.json()
            for project in search_response['projects']:
                if name_pattern.match(project['name']): # search for project name that matches dataset name
                    # scrape
                    project_url = project['urls']['web']['project']
                    scrape_results = scrape_from_url(project_url)
                    X.append(scrape_results)
                    num_label = label_to_number(text_label)
                    Y.append(num_label)
    return X, Y


def scrape_from_url(project_url):
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
    page = requests.get(project_url)
    tree = html.fromstring(page.content)
    # get content
    try:
        data['category'] = tree.xpath('//a[@class="nowrap navy-700 flex items-center medium mr3 type-12"]/text()')[0]
    except:
        pass
    try:
        data['title'] = tree.xpath('//div[@class="col-20-24 col-lg-15-24 hide block-md order-2-md"]//h2/text()')[0]
    except:
        pass
    try:
        data['blurb'] = tree.xpath('//div[@class="col-20-24 col-lg-15-24 hide block-md order-2-md"]//p/text()')[0]
    except:
        pass
    try:
        time1 = tree.xpath('//div[@class="NS_campaigns__funding_period"]//p//time[1]/@datetime')[0]
        time2 = tree.xpath('//div[@class="NS_campaigns__funding_period"]//p//time[2]/@datetime')[0]
        data['duration'] = get_duration(time1, time2)
    except:
        pass
    try:
        data['goal'] = tree.xpath('//div[@id="pledged"]/@data-goal')[0]
    except:
        pass
    try:
        data['raised'] = tree.xpath('//div[@id="pledged"]/@data-pledged')[0]
    except:
        pass
    try:
        data['description'] = ''.join(tree.xpath('//div[@class="full-description js-full-description responsive-media formatted-lists"]//p/text()'))
        # text_to_word_sequence(data['description'])
    except:
        pass
    try:
        data['risks'] = ''.join(tree.xpath('//div[@class="mb3 mb10-sm mb3 js-risks"]//p/text()'))
    except:
        pass
    try:
        data['name'] = tree.xpath('//a[@class="medium navy-700 remote_modal_dialog"]/text()')[0]
    except:
        pass
    # clean
    for key in data:
        data[key] = data[key].replace('\n', ' ').strip()

    # return
    return data


def label_to_number(text_label): # text_label is success=0, failed=1, canceled=2 (sic)
    if text_label == 'successful':
        num_label = 0
    elif text_label == 'failed':
        num_label = 1
    elif text_label == 'canceled':
        num_label = 2
    return num_label


def get_duration(time1, time2):
    # convert string to datetime
    t1 = datetime.strptime(time1[0:18], '%Y-%m-%dT%H:%M:%S')
    t2 = datetime.strptime(time2[0:18], '%Y-%m-%dT%H:%M:%S')
    # get delta
    t3 = t2 - t1
    # return
    return(str(t3.total_seconds()))

