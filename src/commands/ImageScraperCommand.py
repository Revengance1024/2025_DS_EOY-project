import re
import urllib
from typing import Optional
from urllib.parse import urljoin
import os

import bs4
from cleo.helpers import option
from bs4 import BeautifulSoup, PageElement, Tag, NavigableString

from commands.AbstractCommand import AbstractCommand
from modules.DuckDuckGoModule import DuckDuckGoModule
from request_handler.AbstractRequestHandler import AbstractRequestHandler
from request_handler.DefaultRequestHandler import DefaultRequestHandler
from request_handler.SeleniumRequestHandler import SeleniumRequestHandler
from utils.DownloadHelper import DownloadHelper
from utils.Exceptions import UnsupportedOptionCombination
from utils.ImageHelper import ImageHelper


class ImageScraperCommand(AbstractCommand):
    name = 'image-scraper'
    description = 'Scrape Images from url'
    arguments = []
    options = [
        option(
            'follow-links',
            'F',
            description='Follow links on the page',
            flag=True,
        ),
        option(
            'output-dir',
            'd',
            description='Directory to save images',
            flag=False,
            default='output/scraped_images',
        ),
        option(
            'from-har',
            None,
            description='Make initial request from HAR file',
            flag=False,
            default=False,
        ),
        option(
            'from-url',
            None,
            description='Make initial request to provided URL',
            flag=False,
            default=False,
        ),
        option(
            'search',
            None,
            description='Provide search term to use in DuckDuckGo image search',
            flag=False,
            default=False,
        ),
        option(
            'selenium',
            's',
            description='Use selenium. Useful if content is loaded by JS',
            flag=True,
        ),
        option(
            'download-threads',
            None,
            description='Number of threads to use for downloading images',
            flag=False,
            default=8,
        )
    ]
    base_url: str = ""
    request_handler: AbstractRequestHandler = None
    image_progress = {
        "success_images": 0,
        "failed_images": 0,
        "skipped_images": 0,
    }

    def handle(self):
        if self.option('selenium'):
            self.request_handler = SeleniumRequestHandler(self.io)
        else:
            self.request_handler = DefaultRequestHandler(self.io)

        output_dir = self.option('output-dir')
        os.makedirs(output_dir, exist_ok=True)
        self.line_verbose('Image output: ' + os.path.abspath(output_dir))

        soup = self.get_soup()
        self.base_url = self.request_handler.base_url
        images = soup.find_all('img')
        img_urls = []
        img_map = {}  # TODO: Add custom data structure to map image names to URLs

        img: PageElement | Tag | NavigableString
        for img in images:
            img_url = img.get('src')
            if not img_url:
                img_url = img.get('data-src')
            if not img_url:
                self.line_error(f"img does not have src or data-src attribute")
                continue
            img_url = urljoin(self.base_url, img_url)
            img_urls.append(img_url)
            img_name = self.get_image_name(img_url, img)
            if img_name:
                img_map[img_url] = img_name

        total_images = len(img_urls)
        self.line(f"Found {total_images} images on the page. Starting extraction...")
        self.init_progress_bar()
        self.active_progress_bar.start(total_images)

        dl_helper = DownloadHelper(img_urls,
                                   name_map=img_map,
                                   output_dir=output_dir,
                                   status_callback=self.progress_scraper,
                                   max_threads=int(self.option('download-threads')))
        dl_helper.download_files()

        self.active_progress_bar.finish()
        self.active_progress_bar = None
        self.line(f"\nSaved {self.image_progress.get('success_images')}/{total_images} images to {output_dir}")


    def progress_scraper(self, metadata):

        if metadata.get('status') == 'complete':
            self.image_progress['success_images'] += 1
            self.line_verbose(f"Saved image: {metadata.get('image_path')}")
        elif metadata.get('status') == 'failed':
            self.image_progress['failed_images'] += 1
            self.line_error(f"Failed to download image: {metadata.get('error')}")
        else:
            self.line_error(f"Unknown status: {metadata.get('status')}")
            return

        if self.active_progress_bar:
            self.active_progress_bar.set_message(str(self.image_progress.get("success_images")), "success")
            self.active_progress_bar.set_message(str(self.image_progress.get("failed_images")), "failed")
            self.active_progress_bar.set_message(str(self.image_progress.get("skipped_images")), "skipped")
            self.active_progress_bar.advance()


    def get_soup(self) -> BeautifulSoup:
        if self.option('from-url'):
            response_body = self.request_handler.get_page(self.option('from-url'))
        elif self.option('from-har'):
            response_body = self.request_handler.get_page_by_har(self.option('from-har'))
        elif self.option('search'):
            url = "https://duckduckgo.com/?q=" + self.option('search') + "&iax=images&ia=images"
            self.line(f"Opening website: {url}")
            response_body = self.request_handler.get_page(url)
        else:
            raise UnsupportedOptionCombination("from-url or from-har is required")

        return BeautifulSoup(response_body, 'html.parser')

    def init_progress_bar(self):
        self.image_progress = {
            "success_images": 0,
            "failed_images": 0,
            "skipped_images": 0,
        }
        self.active_progress_bar = self.progress_bar()
        self.active_progress_bar.set_format(" %current%/%max% [%bar%] %percent:3s%% %elapsed:6s%/%remaining:-6s% [Success: %success%, Failed: %failed%, Skipped: %skipped%]")
        self.active_progress_bar.set_message("0", "success")
        self.active_progress_bar.set_message("0", "failed")
        self.active_progress_bar.set_message("0", "skipped")


    existing_image_names = set()

    def get_image_name(self, img_url: str, img: Tag) -> Optional[str]:
        parsed_url = urllib.parse.urlparse(img_url)
        original_filename = parsed_url.path.split('/')[-1]

        if ImageHelper.is_img_filename(original_filename):
            name = original_filename
        elif img.get('alt'):
            name = img.get('alt').replace(' ', '_').replace('/', '_').lower()
            name = re.sub(r'\W', '', name)[:50]
            if name in self.existing_image_names:
                name = f"{name}_{len(self.existing_image_names)}"
        else:
            return None

        self.existing_image_names.add(name)

        return name
