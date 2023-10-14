from interfaces.types import SlackMessage


def echo(event: SlackMessage, say):
    say(text=event.ts * 2)
