import json
from urllib.parse import urlencode

import requests


class HarHelper:


    @staticmethod
    def request_from_har(har_file_path) -> requests.Response:
        with open(har_file_path, 'r') as har_file:
            har_data = json.load(har_file)

        entry = har_data['log']['entries'][0]
        request_data = entry['request']

        url = request_data['url']
        method = request_data['method'].lower()
        headers = {header['name']: header['value'] for header in request_data['headers']}
        params = {param['name']: param['value'] for param in request_data.get('queryString', [])}

        headers['Accept-Encoding'] = 'identity'

        return requests.request(method, url, headers=headers, params=params)


    @staticmethod
    def url_from_har(har_file_path) -> str:
        with open(har_file_path, 'r') as har_file:
            har_data = json.load(har_file)

        entry = har_data['log']['entries'][0]
        request_data = entry['request']

        query_params = {param['name']: param['value'] for param in request_data.get('queryString', [])}
        url = request_data['url']

        if query_params:
            url = f"{url}&{urlencode(query_params)}" if "?" in url else f"{url}?{urlencode(query_params)}"

        return url
