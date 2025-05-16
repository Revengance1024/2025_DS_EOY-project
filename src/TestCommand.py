import mimetypes

from exiftool import ExifTool, exiftool

from commands.AbstractCommand import AbstractCommand


class TestCommand(AbstractCommand):

    name = 'test'
    description = 'Command for testing and debugging'
    arguments = []
    options = []

    @staticmethod
    def get_extension(file_path):
        with exiftool.ExifTool() as et:
            output = et.execute("-MIMEType", file_path)
            mime_line = output.strip()
            mime_type = mime_line.split(":")[1].strip() if ":" in mime_line else None
            ext = mimetypes.guess_extension(mime_type)

        return ext

    def handle(self):
        # vb = VirtualBrowser(None)
        #
        # vb.make_request("https://duckduckgo.com/?t=ffab&q=broken+computer&ia=images&iax=images")
        #
        # print("loaded")
        # time.sleep(60)

        with ExifTool(executable='/usr/bin/exiftool') as et:
            # print(et.execute('/home/andrisbremanis/Documents/rtu-projects-sem2/ds/eoy-project/output/scraped_images/3ef3d4c4-1377-4873-9280-14da838da77c'))
            print(self.get_extension('/home/andrisbremanis/Documents/rtu-projects-sem2/ds/eoy-project/output/scraped_images/3ef3d4c4-1377-4873-9280-14da838da77c'))
