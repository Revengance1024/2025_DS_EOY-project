from cleo.application import Application

from commands.ImageScraperCommand import ImageScraperCommand
from TestCommand import TestCommand

application = Application()
application.add(ImageScraperCommand())
application.add(TestCommand())

if __name__ == "__main__":
    application.run()
