from type.type import CommandRoutingConfig
import argparse

from typing import Any, Callable
import sys


class RaiseArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help(sys.stderr)
        raise parse_and_check_args.ArgumentError(None, message)


def is_command(args: list[str], route_config: list[CommandRoutingConfig]):
    first_arg = args[0] if len(args[0]) > 0 else None
    first_arg_is_command = next(
        (config for config in route_config if first_arg == config.command), None
    )
    return first_arg_is_command is not None


def parse_message_event_to_command_if_match(
    args: list[str], route_config: list[CommandRoutingConfig]
) -> tuple[Any, Callable] | tuple[None, None]:
    """_summary_
    Args:
        args (list[str]): _description_
        route_config (_type_): _description_

    Returns:
        _type_: _description_
    """
    cmd = args[0]
    parse_config = next(
        (config for config in route_config if cmd == config.command), None
    )
    if parse_config is None:
        return None, None

    parser = RaiseArgumentParser(description=parse_config.description)
    parser.add_argument("command")
    for arg in parse_config.args:
        parser.add_argument(arg)
    for option in parse_config.options:
        parser.add_argument("--" + option)

    parsed_args = parser.parse_args(args)
    return parsed_args, parse_config.handler
