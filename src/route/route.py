from slack_bolt import App, Say
from type.type import MentionEventHandlerArgs, MentionBody, MentionEvent
from .arg_parser import parse_message_event_to_command_if_match
from .route_config import route_config
import re
from modules.bolt.reply import reply


# "bot_message" サブタイプのメッセージを抽出するリスナーミドルウェア
def no_bot_messages(message, next):
    subtype = message.get("subtype")
    if subtype != "bot_message":
        next()


def extract_mention_and_text(input_string: str) -> dict[str, str]:
    # 正規表現を使用してメンションとテキストを抽出
    mention_pattern = r"<@([^>]+)>"
    mention_match = re.search(mention_pattern, input_string)

    if mention_match:
        mention = "@" + mention_match.group(1)
        text = re.sub(mention_pattern, "", input_string).strip()
    else:
        mention = None
        text = input_string.strip()

    result = {"mention": mention, "text": text}

    return result


def listen(app: App):
    @app.event(event="message", middleware=[no_bot_messages])
    def message_handler(event, say: Say):
        app.logger.info(event)

    @app.event("app_mention")
    def handle_app_mention_events(body):
        mention_body = MentionBody(**body)
        mention_body.event = MentionEvent(**body["event"])
        mention_content = extract_mention_and_text(mention_body.event.text)
        mention_text = mention_content["text"]
        raw_args = mention_text.split(" ")
        try:
            args, handler = parse_message_event_to_command_if_match(
                raw_args, route_config
            )

            if args is not None and handler is not None:
                handler(MentionEventHandlerArgs(app=app, args=args, event=mention_body))
        except BaseException as e:
            app.logger.error(str(e))
            reply(
                app=app,
                mention_body=mention_body,
                text=str(str(e)),
            )
