import os

from nemdata.downloader import download
from nemdata.loader import load

home = os.path.join(os.path.expanduser("~"), "nem-data")


__all__ = ["download", "load"]
