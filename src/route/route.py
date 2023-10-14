from features.echo import echo
from features.echo_block import echo_block
from features.head_sheet import head_sheet
from slack_bolt import App, Say
from type.type import MessageEvent, RoutingConfig, MessageEventHandlerArgs
import argparse

route_config: list[RoutingConfig] = [
    RoutingConfig(
        command="echo",
        description="reply with user input.",
        args=["user_input"],
        options=[],
        handler=echo,
    ),
    RoutingConfig(
        command="echo_block",
        description="show block.",
        args=[],
        options=[],
        handler=echo_block,
    ),
    RoutingConfig(
        command="head_sheet",
        description="reply with spreadsheet data",
        args=[],
        options=[],
        handler=head_sheet,
    ),
]

def parse_message_event_to_command_if_match(args: list[str], route_config: list[RoutingConfig]):
    """_summary_

    Args:
        args (list[str]): _description_
        route_config (_type_): _description_

    Returns:
        _type_: _description_
    """
    cmd = args[0]
    parse_config = next((config for config in route_config if cmd == config.command), None)
    if parse_config is None:
        return None, None

    parser = argparse.ArgumentParser(description=parse_config.description)
    parser.add_argument("command")
    for arg in parse_config.args:
        parser.add_argument(arg)
    for option in parse_config.options:
        parser.add_argument('--' + option)

    parsed_args = parser.parse_args(args)
    return parsed_args, parse_config.handler


# "bot_message" サブタイプのメッセージを抽出するリスナーミドルウェア
def no_bot_messages(message, next):
    subtype = message.get("subtype")
    if subtype != "bot_message":
        next()


def listen(app: App):
    @app.event(event="message", middleware=[no_bot_messages])
    def message_handler(event, say: Say):
        message_event = MessageEvent(**event)
        raw_args = message_event.text.split(" ")
        args, handler = parse_message_event_to_command_if_match(raw_args, route_config)
        if args is not None and handler is not None:
            handler(MessageEventHandlerArgs(args=args, event=message_event, say=say))
