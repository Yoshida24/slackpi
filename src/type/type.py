from dataclasses import dataclass
from typing import Callable
from slack_bolt import App, Say
from typing import Any


@dataclass
class MentionEvent:
    blocks: list[dict]
    channel: str = ""
    client_msg_id: str = ""
    event_ts: str = ""
    parent_user_id: str | None = None
    team: str = ""
    text: str = ""
    thread_ts: str | None = None
    ts: str = ""
    type: str = ""
    user: str = ""


@dataclass
class MentionBody:
    token: str
    team_id: str
    api_app_id: str
    event: MentionEvent
    type: str
    event_id: str
    event_time: int
    authorizations: list[dict]
    is_ext_shared_channel: bool
    event_context: str


@dataclass
class MentionEventHandlerArgs:
    args: Any
    event: MentionBody
    app: App


@dataclass
class RoutingConfig:
    command: str
    description: str
    args: list[str]
    options: list[str]
    handler: Callable[[MentionEventHandlerArgs], None]
