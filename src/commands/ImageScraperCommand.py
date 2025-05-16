import uuid
import json
from urllib.parse import urljoin
import os

from cleo.helpers import option
from bs4 import BeautifulSoup
import requests
from cleo.io.io import IO

from commands.AbstractCommand import AbstractCommand
from request_handler.AbstractRequestHandler import AbstractRequestHandler
from request_handler.DefaultRequestHandler import DefaultRequestHandler
from request_handler.SeleniumRequestHandler import SeleniumRequestHandler
from utils.Exceptions import SkipException, UnsupportedOptionCombination
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
            'output-html',
            None,
            description='File to save HTML for debugging purposes',
            flag=False,
            default='output/response.html',
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
            'selenium',
            's',
            description='Use selenium. Useful if content is loaded by JS',
            flag=True,
        )
    ]

    base_url: str = ""
    request_handler: AbstractRequestHandler = None

    def initialize(self, io: IO) -> None:
        if self.option('selenium'):
            self.request_handler = SeleniumRequestHandler(self.io)
        else:
            self.request_handler = DefaultRequestHandler(self.io)

    def handle(self):
        output_dir = self.option('output-dir')
        os.makedirs(output_dir, exist_ok=True)
        self.line_verbose('Image output: ' + os.path.abspath(output_dir))

        soup = self.get_soup()
        images = soup.find_all('img')
        total_images = len(images)

        self.line(f"Found {total_images} images on the page. Starting extraction...")
        self.init_progress_bar()
        self.active_progress_bar.start(total_images)
        success_images = 0
        failed_images = 0
        skipped_images = 0

        for img in images:
            try:
                img_url = img.get('src')

                if not img_url:
                    raise Exception("Image url not set")

                img_url = urljoin(self.base_url, img_url)
                # parsed_url = urlparse(img_url)

                # if parsed_url.path:
                #     print(parsed_url.path)
                #     img_name = os.path.basename(parsed_url.path)
                #     img_type = os.path.splitext(img_name)[1].lstrip('.')
                # else:
                img_name = str(uuid.uuid4())
                img_data = requests.get(img_url).content
                img_path = os.path.join(output_dir, img_name)

                with open(img_path, 'wb') as img_file:
                    img_file.write(img_data)

                img_type = ImageHelper.fix_image_extension(img_path)

                metadata = {
                    'original_url': img_url,
                    'image_type': img_type,
                    'original_name': img_name
                }
                json_path = os.path.join(output_dir, f"{os.path.splitext(img_name)[0]}.json")

                with open(json_path, 'w') as json_file:
                    json.dump(metadata, json_file, indent=4)

                success_images += 1
                self.active_progress_bar.set_message(str(success_images), "success")
                self.line_verbose(f"Saved image: {img_name}")

            except SkipException:
                skipped_images += 1
                self.active_progress_bar.set_message(str(skipped_images), "skipped")
            except Exception as e:
                failed_images += 1
                self.active_progress_bar.set_message(str(failed_images), "failed")
                self.line_error(f"Failed to download image: {e}")
            finally:
                self.active_progress_bar.advance()

        self.active_progress_bar.finish()
        self.active_progress_bar = None
        self.line(f"\nSaved {success_images}/{total_images} images and metadata to {output_dir}")


    def get_soup(self) -> BeautifulSoup:
        if self.option('from-url'):
            response_body = self.request_handler.get_page(self.option('from-url'))
        elif self.option('from-har'):
            response_body = self.request_handler.get_page_by_har(self.option('from-har'))
        else:
            raise UnsupportedOptionCombination("from-url or from-har is required")

        return BeautifulSoup(response_body, 'html.parser')

    def init_progress_bar(self):
        self.active_progress_bar = self.progress_bar()
        self.active_progress_bar.set_format(" %current%/%max% [%bar%] %percent:3s%% %elapsed:6s%/%estimated:-6s% [Success: %success%, Failed: %failed%, Skipped: %skipped%]")
        self.active_progress_bar.set_message("0", "success")
        self.active_progress_bar.set_message("0", "failed")
        self.active_progress_bar.set_message("0", "skipped")
