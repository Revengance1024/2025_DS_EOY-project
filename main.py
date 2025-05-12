from cleo.application import Application

from image_scraper.ImageScraperCommand import ImageScraperCommand

application = Application()
application.add(ImageScraperCommand())

if __name__ == "__main__":
    application.run()
