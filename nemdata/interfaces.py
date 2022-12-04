import sys
import zipfile

import requests

header = {"user-agent": "Adam Green, adam.green@adgefficiency.com"}


def scrape_url(url, output_file):
    """Downloads a file from a url using requests"""
    response = requests.get(url, headers=header, stream=True)
    if response.status_code != 200:
        print(f"not found, {url}")
        return None

    print(f"downloaded, {url}")
    with open(output_file, "wb") as f:

        total_length = response.headers.get("content-length")
        if total_length is None:
            #  no content length header
            f.write(response.content)
        else:
            #  download with progress bar
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write(
                    "\r {}% [{}{}]".format(2 * done, "+" * done, " " * (50 - done))
                )
                sys.stdout.flush()
    print(" ")
    return True


def unzip_file(file_path, output_path):
    """unzips a file from one path to an output path using stdlib"""
    try:
        with zipfile.ZipFile(file_path, "r") as my_zipfile:
            my_zipfile.extractall(output_path)
    except zipfile.BadZipFile:
        print("{} not a ZipFile".format(file_path))
