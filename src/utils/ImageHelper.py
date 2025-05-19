import mimetypes
import os

from exiftool import ExifTool

class ImageHelper:

    @staticmethod
    def fix_image_extension(image_path):
        if ImageHelper.is_img_filename(image_path):
            return None

        ext = ImageHelper.get_extension(image_path)
        if ext:
            new_image_path = f"{image_path}{ext}"
            os.rename(image_path, new_image_path)
            return ext

        return None

    @staticmethod
    def get_extension(file_path):
        with ExifTool() as et:
            output = et.execute("-MIMEType", file_path)
            mime_line = output.strip()
            mime_type = mime_line.split(":")[1].strip() if ":" in mime_line else None
            ext = mimetypes.guess_extension(mime_type)

        return ext

    @staticmethod
    def is_img_filename(file_path: str) -> bool:
        original_filename = file_path.split('/')[-1]
        if not original_filename:
            return False
        recognized_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp']
        ext = original_filename.split('.')[-1].lower()
        return ext in recognized_extensions