import json
from typing import Optional
from urllib.parse import urlencode, urlparse

import requests
from cleo.io.io import IO

from request_handler.AbstractRequestHandler import AbstractRequestHandler
from utils.Exceptions import InvalidResponseException


class DefaultRequestHandler(AbstractRequestHandler):
    session: Optional[requests.Session] = None

    def __init__(self, io: IO):
        super().__init__(io)

        self.session = requests.Session()

        # add some default headers to avoid simple bot detection
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/138.0",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/*,*/*;q=0.8",
            "Connection": "keep-alive",
        })

    def get_page(self, url: str, extra: Optional[dict] = None) -> str:
        if extra and extra.get('query_params'):
            query_params = extra.get('query_params')
            url = f"{url}&{urlencode(query_params)}" if "?" in url else f"{url}?{urlencode(query_params)}"

        response = self.session.get(url, allow_redirects=True)

        return self.handle_response(response)

    def get_page_by_har(self, har_file_path: str) -> str:
        with open(har_file_path, 'r') as har_file:
            har_data = json.load(har_file)

        request_data = har_data['log']['entries'][0]['request']
        url = request_data['url']
        headers = {header['name']: header['value'] for header in request_data['headers']}
        params = {param['name']: param['value'] for param in request_data.get('queryString', [])}
        # override the Accept-Encoding header to avoid gzip encoding
        headers['Accept-Encoding'] = 'identity'

        response = self.session.get(url, headers=headers, params=params)

        return self.handle_response(response)

    def handle_response(self, response: requests.Response) -> str:
        # responses between 200 and 299 are considered successful
        if response.status_code < 200 or response.status_code > 299:
            raise InvalidResponseException("Received invalid status code: " + str(response.status_code))

        parsed_url = urlparse(response.url)
        self.base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

        return response.text
