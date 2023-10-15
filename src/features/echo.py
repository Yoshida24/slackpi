from type.type import MentionEventHandlerArgs
from modules.bolt.reply import reply


def echo(args: MentionEventHandlerArgs) -> None:
    reply(
        args.app,
        mention_body=args.event,
        text=f"{args.event.event.text} <@{args.event.event.user}>",
    )
