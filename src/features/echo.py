from type.type import MessageEventHandlerArgs


def echo(args: MessageEventHandlerArgs) -> None:
    args.say(text=f"{args.args.user_input} <@{args.event.user}>")
