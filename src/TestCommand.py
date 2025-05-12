import time
from typing import Optional

from cleo.helpers import option
from cleo.ui.progress_bar import ProgressBar
from bs4 import BeautifulSoup
import os
import requests
import json
from urllib.parse import urljoin, urlparse

from AbstractCommand import AbstractCommand
from image_scraper.VirtualBrowser import VirtualBrowser
from utils.HarHelper import HarHelper


class TestCommand(AbstractCommand):

    name = 'test'
    description = 'Command for testing and debugging'
    arguments = []
    options = []


    def handle(self):
        vb = VirtualBrowser(None)

        vb.make_request("https://duckduckgo.com/?t=ffab&q=broken+computer&ia=images&iax=images")

        print("loaded")
        time.sleep(60)
