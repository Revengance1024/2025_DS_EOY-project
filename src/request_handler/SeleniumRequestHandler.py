import time
from typing import Optional
from urllib.parse import urlencode, urlparse

from cleo.io.io import IO
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from request_handler.AbstractRequestHandler import AbstractRequestHandler

class SeleniumRequestHandler(AbstractRequestHandler):

    def __init__(self, io: IO, headless: bool = False):
        super().__init__(io)

        options = uc.ChromeOptions()
        options.headless = headless
        options.add_argument("--window-size=1920,1080")
        self.driver = uc.Chrome(options=options)

    def get_page(self, url: str, extra: Optional[dict] = None) -> str:
        if extra and extra.get('query_params'):
            query_params = extra.get('query_params')
            url = f"{url}&{urlencode(query_params)}" if "?" in url else f"{url}?{urlencode(query_params)}"

        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(
            # Wait until we load at least 10 images to detect if JS has loaded the image HTML
            lambda d: len(d.find_elements(By.CSS_SELECTOR, "img")) >= 10
        )

        self.driver.save_screenshot('screenshot.png')

        parsed_url = urlparse(self.driver.current_url)
        self.base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

        return self.driver.page_source
