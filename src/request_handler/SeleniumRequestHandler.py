from typing import Optional
from urllib.parse import urlencode, urlparse

from cleo.io.io import IO
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from request_handler.AbstractRequestHandler import AbstractRequestHandler

class SeleniumRequestHandler(AbstractRequestHandler):

    def __init__(self, io: IO, driver_path: Optional[str] = None):
        super().__init__(io)

        chrome_options = Options()
        self.driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)

    def get_page(self, url: str, extra: Optional[dict] = None) -> str:
        if extra.get('query_params'):
            query_params = extra.get('query_params')
            url = f"{url}&{urlencode(query_params)}" if "?" in url else f"{url}?{urlencode(query_params)}"

        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(
            lambda d: len(d.execute_script('return document.getElementById("react-layout")?.innerHTML')) > 10
        )

        parsed_url = urlparse(self.driver.current_url)
        self.base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

        return self.driver.page_source

    def __del__(self):
        if self.driver:
            self.driver.close()