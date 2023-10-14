from modules.bolt.listener import ActionDef
from features.echo import echo
from features.echo_block import echo_block
from features.read_from_sheet import read_from_sheet
from slack_bolt import App
import re
from interfaces.types import SlackMessage


# "bot_message" サブタイプのメッセージを抽出するリスナーミドルウェア
def no_bot_messages(message, next):
    subtype = message.get("subtype")
    if subtype != "bot_message":
        next()


def listen_message(app: App):
    @app.event(event="message", middleware=[no_bot_messages])
    def message_handler(event, say):
        evt = SlackMessage(**event)
        from pprint import pprint

        pprint(evt)
        print(evt)
        read_from_sheet(evt, say)


def listen_action(app: App, action_defs: list[ActionDef]):
    @app.action(re.compile(""))
    def action_handler(body, ack, say):
        for action_def in action_defs:
            action_id = body["actions"][0]["action_id"]
            if action_id == action_def.id:
                value = body["actions"][0]["selected_option"]["value"]  # value-N
                say(action_def.text + value)
                ack()
