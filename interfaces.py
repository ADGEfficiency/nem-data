import os
import zipfile
import sys
import bs4
import requests


header = {'user-agent': 'Adam Green, adam.green@adgefficiency.com'}


def scrape_url(url, output_path):
    with open(output_path, 'wb') as f:
        response = requests.get(url, headers=header, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None: # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write('\r {}% [{}{}]'.format(2*done, '+'*done, ' '*(50-done)))
                sys.stdout.flush()


def unzip_file(file_path, output_path):
    with zipfile.ZipFile(file_path, 'r') as my_zipfile:
        my_zipfile.extractall(output_path)
