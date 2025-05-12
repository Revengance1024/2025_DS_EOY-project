from cleo.helpers import argument, option
from cleo.commands.command import Command

class ImageScraperCommand(Command):

    name = 'image-scraper'
    description = 'Scrape Images from url'
    arguments = [
        argument(
            'url',
            description='URL of the initial page'
        )
    ]

    options = [
        option(
            'follow-links',
            'F',
            description='Follow links on the page',
            flag=True
        )
    ]

    def handle(self):
        print('Scraping images from url ' + self.argument('url'))
