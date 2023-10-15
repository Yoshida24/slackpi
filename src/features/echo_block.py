from type.type import MentionEventHandlerArgs
from modules.bolt.reply import reply


def echo_block(args: MentionEventHandlerArgs) -> None:
    reply(
        app=args.app,
        mention_body=args.event,
        text=f"Hey there <@{args.event.event.user}>!",
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Hey there <@{args.event.event.user}>!",
                },
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click Me"},
                    "action_id": "button_click",
                },
            }
        ],
    )
