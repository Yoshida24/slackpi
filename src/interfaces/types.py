from dataclasses import dataclass


@dataclass
class SlackMessage:
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
