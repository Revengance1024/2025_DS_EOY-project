from cleo.commands.command import Command
from cleo.io.outputs.output import Verbosity


class AbstractCommand(Command):


    def line_debug(self, message: str) -> None:
        self.line(message, verbosity=Verbosity.DEBUG)


    def line_verbose(self, message: str) -> None:
        self.line(message, verbosity=Verbosity.VERBOSE)
