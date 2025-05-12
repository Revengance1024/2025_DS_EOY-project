import time
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from urllib.parse import urlencode


class VirtualBrowser:

    def __init__(self, driver_path: Optional[str] = None):
        chrome_options = Options()
        self.driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)


    def make_request(self, url: str, query_params: dict = None) -> BeautifulSoup:
        if query_params:
            # append query params even if url already has query params
            url = f"{url}&{urlencode(query_params)}" if "?" in url else f"{url}?{urlencode(query_params)}"

        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )

        time.sleep(5)

        return BeautifulSoup(self.driver.page_source, 'html.parser')


    def close(self):
        self.driver.quit()
