from collections import namedtuple
import requests


URL = namedtuple("url", "url, year, month, report, csv, xml, home")


def download_zipfile_from_url(url, chunk_size=128):
    path = url.home / "raw.zip"
    print(f" downloading zip to {path}")
    r = requests.get(url.url, stream=True)
    with open(path, "wb") as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)
    return path


def unzip(path):
    import zipfile

    with zipfile.ZipFile(path, "r") as zip_ref:
        zip_ref.extractall(path.parent)
