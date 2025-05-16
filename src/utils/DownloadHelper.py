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
                 max_threads: int = 8):
        self.urls: list[str] = urls
        self.output_dir: str = output_dir
        self.name_map: Optional[dict[str, str]] = name_map
        self.max_threads: int = max_threads
        self.io: Optional[IO] = None
        self.download_map: dict[str, dict[str, str]] = {}

    def download_file(self, img_url) -> dict[str, str]:
        img_name = str(uuid.uuid4())
        img_data = requests.get(img_url).content
        img_path = os.path.join(self.output_dir, img_name)

        with open(img_path, 'wb') as img_file:
            img_file.write(img_data)

        img_type = ImageHelper.fix_image_extension(img_path)

        metadata = {
            'original_url': img_url,
            'original_name': img_name,
            'image_path': img_path,
            'image_type': img_type,
        }
        # json_path = os.path.join(self.output_dir, f"{os.path.splitext(img_name)[0]}.json")
        #
        # with open(json_path, 'w') as json_file:
        #     json.dump(metadata, json_file, indent=4)

        return metadata

    def download_files(self) -> list[dict[str, str]]:

        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            return list(executor.map(self.download_file, self.urls))
