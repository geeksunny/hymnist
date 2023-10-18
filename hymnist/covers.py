__dimension_limit_default__ = [1000, 600, 360]
__default_dimension_default__ = 600
__dpi_default__ = 72

from typing import Tuple

from hymnist.args import ArgParseMixin, Argument, ArgumentsProvider


class Covers(ArgParseMixin):

    def __init__(self, arguments_provider: ArgumentsProvider = None) -> None:
        super().__init__(arguments_provider)

    def _get_args_name_and_desc(self) -> Tuple[str | None, str | None]:
        return "Cover-Art Conditioning", "Process existing cover-art files."

    def _get_arguments(self) -> Tuple[Argument, ...] | Argument:
        return (
            Argument(('-m', '--missing'),
                     help='Find all albums that do not have a cover.jpg file.',
                     action='store_true'),
            Argument('dimension_limit',
                     nargs='*',
                     help='Max height/width to make resized copies at.',
                     default=__dimension_limit_default__),
            Argument(('-d', '--default-dimension'),
                     help='Max height/width to use for the default cover.jpg.',
                     default=__default_dimension_default__),
            Argument('--dpi',
                     help='DPI for resized images.',
                     default=__dpi_default__)
        )
