from slack_bolt import App, Say
from type.type import MentionEventHandlerArgs, MentionBody, MentionEvent
from .arg_parser import parse_message_event_to_command_if_match, is_command
from .route_config import route_config
import re
from modules.bolt.reply import reply
from modules.bolt.get_conversations import get_conversations
from modules.bolt.extract_mention_and_text import extract_mention_and_text


# "bot_message" サブタイプのメッセージを抽出するリスナーミドルウェア
def no_bot_messages(message, next):
    subtype = message.get("subtype")
    if subtype != "bot_message":
        next()


def listen(app: App):
    @app.event(event="message", middleware=[no_bot_messages])
    def message_handler(event, say: Say):
        app.logger.info(event)

    @app.event("app_mention")
    def handle_app_mention_events(body):
        mention_body = MentionBody(**body)
        mention_body.event = MentionEvent(**body["event"])
        # chack is message is command,
        raw_args = extract_mention_and_text(mention_body.event.text)["text"].split(
            " "
        )  # ["text", "separated", "by", "space"]
        if is_command(raw_args, route_config.command_routing_configs):
            # In case of command, parse message to args and call handler
            try:
                args, command_handler = parse_message_event_to_command_if_match(
                    raw_args, route_config.command_routing_configs
                )
                if args is not None and command_handler is not None:
                    command_handler(
                        MentionEventHandlerArgs(app=app, args=args, event=mention_body)
                    )
            except BaseException as e:
                app.logger.error(str(e))
                reply(
                    app=app,
                    mention_body=mention_body,
                    text=str(str(e)),
                )
        else:
            # In case of Unstructured message, LLM Bot will reply
            try:
                messages = get_conversations(
                    app=app,
                    mention_body=mention_body,
                )["messages"]
                route_config.unstructured_message_routing_config.handler(
                    MentionEventHandlerArgs(
                        app=app,
                        args=None,
                        event=mention_body,
                        messages=messages,
                    )
                )
            except Exception as e:
                app.logger.error(f"Error getting thread replies: {str(e)}")
