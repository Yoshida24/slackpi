from dataclasses import dataclass
from typing import Callable

from slack_bolt import Say
from typing import Any

@dataclass
class MessageEvent:
    blocks: list[dict]
    channel: str
    channel_type: str
    client_msg_id: str
    event_ts: float
    parent_user_id: str | None = None
    team: str = ""
    text: str = ""
    thread_ts: str | None = None
    ts: str = ""
    type: str = ""
    user: str = ""


@dataclass
class MessageEventHandlerArgs:
    args: Any
    event: MessageEvent
    say: Say


@dataclass
class RoutingConfig:
    command: str
    description: str
    args: list[str]
    options: list[str]
    handler: Callable[[MessageEventHandlerArgs], None]
