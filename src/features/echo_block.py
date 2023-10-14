from type.type import MessageEventHandlerArgs


def echo_block(args: MessageEventHandlerArgs) -> None:
    args.say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there <@{args.event.user}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click Me"},
                    "action_id": "button_click",
                },
            }
        ],
        text=f"Hey there <@{args.event.user}>!",
    )
