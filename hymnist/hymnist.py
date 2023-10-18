from argparse import HelpFormatter, ArgumentDefaultsHelpFormatter
from typing import Tuple, Type

from hymnist import ArgumentsProvider, Argument
from hymnist import Covers


class Hymnist(ArgumentsProvider):
    _covers: Covers = None

    def __init__(self) -> None:
        super().__init__()

        self._covers = Covers(self)

    @property
    def _argument_help_description(self) -> str | None:
        return 'Tool to execute tasks for processing a local music collection.'

    @property
    def _argument_help_formatter(self) -> Type[HelpFormatter]:
        return ArgumentDefaultsHelpFormatter

    def _get_arguments(self) -> Tuple[Argument, ...] | Argument:
        return (
            Argument('paths',
                     help='Target paths to process.',
                     nargs='+'),
            Argument('--debug',
                     help='Enable debug output.',
                     action='store_true'),
            Argument(('-v', '--verbose'),
                     help='Enable verbose output.',
                     action='store_true')
        )
