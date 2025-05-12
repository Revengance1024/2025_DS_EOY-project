import mimetypes
import os

from exiftool import ExifTool

class ImageHelper:

    @staticmethod
    def fix_image_extension(image_path):
        ext = ImageHelper.get_extension(image_path)
        if ext:
            new_image_path = f"{image_path}{ext}"
            os.rename(image_path, new_image_path)
            return ext

        return "unknown"

    @staticmethod
    def get_extension(file_path):
        with ExifTool() as et:
            output = et.execute("-MIMEType", file_path)
            mime_line = output.strip()
            mime_type = mime_line.split(":")[1].strip() if ":" in mime_line else None
            ext = mimetypes.guess_extension(mime_type)

        return ext