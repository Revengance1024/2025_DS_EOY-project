from typing import Optional

from cleo.io.io import IO


class AbstractRequestHandler:

    io: IO
    base_url: Optional[str] = None

    def __init__(self, io: IO):
        self.io = io

    def get_page(self, url: str, extra: Optional[dict] = None) -> str:
        raise NotImplementedError()

    def get_page_by_har(self, har_file_path: str) -> str:
        raise NotImplementedError()

    def get_absolute_url(self, path: str) -> str:
        if self.base_url is None:
            return f"/{path.lstrip('/')}"
        return f"{self.base_url}/{path.lstrip('/')}"