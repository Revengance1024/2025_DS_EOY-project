from typing import Optional

from cleo.commands.command import Command
from cleo.io.outputs.output import Verbosity
from cleo.ui.progress_bar import ProgressBar


class AbstractCommand(Command):

    active_progress_bar: Optional[ProgressBar] = None

    def line(
            self,
            text: str,
            style: str | None = None,
            verbosity: Verbosity = Verbosity.NORMAL
    ) -> None:
        if self.active_progress_bar:
            self.active_progress_bar.clear()

        Command.line(self, text, style, verbosity)

        if self.active_progress_bar:
            self.active_progress_bar.display()

    def line_debug(self, message: str) -> None:
        self.line(message, verbosity=Verbosity.DEBUG)

    def line_verbose(self, message: str) -> None:
        self.line(message, verbosity=Verbosity.VERBOSE)
