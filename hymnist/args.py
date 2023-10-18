from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, HelpFormatter
from dataclasses import dataclass
from typing import Tuple, Any, Type

from hymnist.utils import PostInitCaller


@dataclass
class Argument:
    name_or_flags: Tuple[str, ...] | str = None
    action: str = None
    nargs: str | int = None
    const: Any = None
    default: Any = None
    type: Any = None
    choices: Any = None
    required: bool = None
    help: str = None
    metavar: str = None
    dest: str = None
    version: str = None

    def __post_init__(self):
        if self.name_or_flags is not None and not isinstance(self.name_or_flags, tuple):
            self.name_or_flags = (self.name_or_flags,)

    def flags_and_kwargs(self, prefix_chars: str | None = None) -> Tuple[str | Tuple[str, ...], dict[str, Any]]:
        dictionary = {k: v for k, v in self.__dict__.items() if v is not None}
        if 'name_or_flags' in dictionary:
            flags = dictionary['name_or_flags']
            if prefix_chars is not None and flags is not None and not flags[0][0] in prefix_chars:
                dictionary['dest'] = flags[0]
                flags = None
            del dictionary['name_or_flags']
        else:
            flags = None
        return flags, dictionary


class ArgumentsProvider(metaclass=PostInitCaller):
    _args: ArgumentParser = None

    def __init__(self):
        self._args = ArgumentParser(description=self._argument_help_description,
                                    formatter_class=self._argument_help_formatter)
        args = self._get_arguments()
        if args is not None:
            self.add_arguments(*args if isinstance(args, tuple) else args)

    def __post_init__(self):
        self._args.parse_args()

    @property
    def _argument_help_description(self) -> str | None:
        """Property that defines this ArgumentsProvider's help description."""

        return None

    @property
    def _argument_help_formatter(self) -> Type[HelpFormatter]:
        """Property that defines the HelpFormatter that ArgumentParser will use.
        Override to use a non-default formatter."""

        return HelpFormatter

    @property
    def args(self):
        return self._args

    def _get_arguments(self) -> Tuple[Argument, ...] | Argument | None:
        """Method to add arguments from this ArgumentProvider object itself.
        Override and return Argument objects if necessary."""

        return None

    def add_arguments(self, *args: Argument, group_name: str = None, group_desc: str = None):
        parser = self._args.add_argument_group(group_name, group_desc)\
            if group_name is not None or group_desc is not None\
            else self._args
        for arg in args:
            flags, kwargs = arg.flags_and_kwargs(self._args.prefix_chars)
            if flags is None:
                parser.add_argument(**kwargs)
            else:
                parser.add_argument(*flags, **kwargs)


class ArgParseMixin:
    """Mixin class to add ArgumentParser arguments specific to the inheriting class."""

    def __init__(self, arguments_provider: ArgumentsProvider = None) -> None:
        super().__init__()
        if arguments_provider is not None:
            args = self._get_arguments()
            name, desc = self._get_args_name_and_desc()
            arguments_provider.add_arguments(*args if isinstance(args, tuple) else args, group_name=name,
                                             group_desc=desc)

    def _get_args_name_and_desc(self) -> Tuple[str | None, str | None]:
        """Method to override if the arguments defined in this class should go under an argument group.
        Return a tuple in the format of (name, description) with at least one value being a string to separate
        this class' arguments into their own argument group."""

        return None, None

    def _get_arguments(self) -> Tuple[Argument, ...] | Argument:
        """Method to add arguments to the supplied ArgumentParser object.
        Must be implemented when self._args is not None."""

        raise NotImplementedError()
