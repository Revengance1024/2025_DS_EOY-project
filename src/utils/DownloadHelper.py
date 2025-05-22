import json
import os
import uuid
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

import requests
from cleo.io.io import IO

from utils.ImageHelper import ImageHelper


class DownloadHelper:
    def __init__(self, urls: list[str], output_dir: str, name_map: Optional[dict[str, str]] = None,
                 max_threads: int = 4, status_callback: Optional[callable] = None):
        self.urls: list[str] = urls
        self.output_dir: str = output_dir
        self.name_map: Optional[dict[str, str]] = name_map
        self.max_threads: int = max_threads
        self.io: Optional[IO] = None
        self.download_map: dict[str, dict[str, str]] = {}
        self.status_callback: Optional[callable] = status_callback

    def download_file(self, img_url) -> dict[str, str]:

        try:
            img_data = requests.get(img_url).content

            if self.name_map and img_url in self.name_map:
                img_name = self.name_map[img_url]
            else:
                img_name = str(uuid.uuid4())
            img_path = os.path.join(self.output_dir, img_name)

            with open(img_path, 'wb') as img_file:
                img_file.write(img_data)

            img_type = ImageHelper.fix_image_extension(img_path)

            if img_type:
                img_path = f"{img_path}{img_type}"

            metadata = {
                'original_url': img_url,
                'original_name': img_name,
                'image_path': img_path,
                'image_type': img_type,
                'status': 'complete',
            }

            if self.status_callback:
                self.status_callback(metadata)

        except Exception as e:
            metadata = {
                'original_url': img_url,
                'status': 'failed',
                'error': str(e),
            }

            if self.status_callback:
                self.status_callback(metadata)

        return metadata

    def download_files(self) -> list[dict[str, str]]:

        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            return list(executor.map(self.download_file, self.urls))
