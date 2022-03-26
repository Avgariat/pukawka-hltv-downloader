#!/usr/local/bin/python3
import urllib.request
import json
import os
import datetime
import shutil


max_weight = 3
keep_for_days = 15
servers_urls = {
    'deathrun_v1': 'http://733166.node23.pukawka.pl/new.txt',
    'deathrun_v2': 'http://733167.node23.pukawka.pl/new.txt',
}
destination_path = os.path.abspath(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        os.pardir
    )
)


def get_size(start_path='.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size


def to_giga_bytes(size_bytes):
    # bytes > KB > MB > GB
    return size_bytes / 1024 / 1024 / 1024


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


def filter_files_list(files_list, dir_path=None):
    if dir_path is None:
        dir_files = os.listdir()
    else:
        if not os.path.isdir(dir_path):
            return files_list.copy()
        else:
            dir_files = os.listdir(dir_path)
    filtered_files = [file for file in files_list if file['name'] not in dir_files]
    return filtered_files


def filter_files_dict(files_dict, dir_path):
    filtered_dict = {}
    for key in files_dict:
        search_path = os.path.join(dir_path, key)
        filtered_dict[key] = filter_files_list(files_dict[key], search_path)
    return filtered_dict


def download_files_list(files_list, dir_path):
    for file_dict in files_list:
        file_name = file_dict['name']
        file_url = file_dict['url']
        output_file = os.path.join(dir_path, file_name)
        download_file(file_url, output_file)


def compute_list_size(files_list):
    size = 0
    for file_dict in files_list:
        size += file_dict['size']
    return size


def download_files_from_dict(files_dict, dir_path):

    for key in files_dict:
        max_size = max_weight - to_giga_bytes(compute_list_size(files_dict[key]))
        current_size = to_giga_bytes(get_size(dir_path))
        if current_size > max_size:
            continue
        dir_date_path = os.path.join(dir_path, key)
        if not os.path.isdir(dir_date_path):
            os.makedirs(dir_date_path, mode=0o755)
        download_files_list(files_dict[key], dir_date_path)


def main_download_recordings(base_url, dir_path):
    try:
        files_dict_by_date = get_json(base_url)
    except ValueError:
        return

    files_dict_by_date = filter_files_dict(files_dict_by_date, dir_path)
    download_files_from_dict(files_dict_by_date, dir_path)


def delete_old_dirs(dir_path):
    if not os.path.isdir(dir_path):
        return
    time_boundary = datetime.datetime.now().replace(hour=0, minute=1) - datetime.timedelta(days=keep_for_days)
    for directory in os.listdir(dir_path):
        directory_path = os.path.join(dir_path, directory)
        if os.path.isdir(directory_path):
            try:
                then = datetime.datetime.strptime(directory, '%Y-%m-%d')
            except ValueError:
                continue
            if then < time_boundary:
                shutil.rmtree(directory_path)


if __name__ == '__main__':
    for server in servers_urls:
        dest_path = os.path.join(destination_path, server)
        delete_old_dirs(dest_path)
        main_download_recordings(servers_urls[server], dest_path)
