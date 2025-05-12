from typing import Optional

from cleo.helpers import option
from cleo.ui.progress_bar import ProgressBar
from bs4 import BeautifulSoup
import os
import requests
import json
from urllib.parse import urljoin, urlparse

from AbstractCommand import AbstractCommand
from utils.HarHelper import HarHelper


class ImageScraperCommand(AbstractCommand):

    name = 'image-scraper'
    description = 'Scrape Images from url'
    arguments = []

    options = [
        option(
            'follow-links',
            'F',
            description='Follow links on the page',
            flag=True
        ),
        option(
            'output-dir',
            'd',
            description='Directory to save images',
            flag=False,
            default='output/scraped_images'
        ),
        option(
            'output-html',
            None,
            description='File to save HTML for debugging purposes',
            flag=False,
            default='output/response.html'
        ),
        option(
            'from-har',
            None,
            description='Make initial request from HAR file',
            flag=False,
            default=False
        ),
        option(
            'from-url',
            None,
            description='Make initial request to provided URL',
            flag=False,
            default=False
        )
    ]


    def perform_request(self) -> Optional[requests.Response]:
        if self.option('from-har'):
            har_file = self.option('from-har')
            if not os.path.exists(har_file):
                self.line_error(f"File {har_file} does not exist")
                return None

            self.line_verbose('Scraping images from HAR file: ' + har_file)
            return HarHelper.request_from_har(har_file)

        if self.option('from-url'):
            self.line_verbose('Scraping images from URL: ' + self.option('from-url'))
            return requests.get(self.option('from-url'))

        return None


    def handle(self):
        output_dir = self.option('output-dir')
        os.makedirs(output_dir, exist_ok=True)
        self.line_verbose('Image output: ' + os.path.abspath(output_dir))

        response = self.perform_request()
        response.encoding = response.apparent_encoding
        self.line_verbose('Got response from URL: ' + response.url)

        if response.status_code != 200:
            self.line_error(f"Failed to fetch from URL: {response.url}, status code: {response.status_code}")
            self.line_error(response.text)
            return

        if self.option('output-html'):
            with open(self.option('output-html'), 'w', encoding='utf-8') as f:
                f.write(response.text)
            self.line_verbose('HTML output: ' + os.path.abspath(self.option('output-html')))

        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img')
        total_images = len(images)

        self.line(f"Found {total_images} images on the page. Starting extraction...")
        progress_bar: ProgressBar = self.progress_bar(total_images)
        failed_images = 0

        for img in images:
            img_url = img.get('src')

            if not img_url:
                failed_images += 1
                self.line_verbose(f"Failed saving image")
                progress_bar.advance()
                continue

            img_url = urljoin(response.url, img_url)
            parsed_url = urlparse(img_url)
            img_name = os.path.basename(parsed_url.path)
            img_type = os.path.splitext(img_name)[1].lstrip('.')

            try:
                img_data = requests.get(img_url).content
                img_path = os.path.join(output_dir, img_name)

                with open(img_path, 'wb') as img_file:
                    img_file.write(img_data)

                metadata = {
                    'original_url': img_url,
                    'image_type': img_type,
                    'original_name': img_name
                }
                json_path = os.path.join(output_dir, f"{os.path.splitext(img_name)[0]}.json")

                with open(json_path, 'w') as json_file:
                    json.dump(metadata, json_file, indent=4)

                self.line_verbose(f"Saved image: {img_name}")

            except Exception as e:
                self.line_error(f"Failed to download image {img_url}: {e}")

            finally:
                progress_bar.advance()

        progress_bar.finish()
        self.line(f"Saved {total_images - failed_images}/{total_images} images and metadata to {output_dir}")
