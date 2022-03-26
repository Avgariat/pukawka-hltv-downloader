#!/usr/local/bin/python3
import urllib.request
import json


link = 'http://733166.node34.pukawka.pl/new.txt'


def get_json(pukawka_url):
    response = urllib.request.urlopen(pukawka_url)
    response_data = response.read()
    response_data = response_data.decode('utf-8')
    response_data = json.loads(response_data)
    return response_data


def download_file(file_url, output_path):
    print('downloading file {}...'.format(output_path))
    with urllib.request.urlopen(file_url) as response, open(output_path, 'wb') as output_file:
        response_data = response.read()
        output_file.write(response_data)


if __name__ == '__main__':
    data = get_json(link)
    data_day = data['2020-06-28']
    data_demo = data_day[0]
    download_file(data_demo['url'], data_demo['name'])
