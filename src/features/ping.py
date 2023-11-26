from type.type import MentionEventHandlerArgs
from modules.bolt.reply import reply
import socket


def handler(args: MentionEventHandlerArgs) -> None:
    ip = get_ip()
    host = get_hostname()
    reply(
        args.app,
        mention_body=args.event,
        blocks=[
            {
                "type": "rich_text",
                "elements": [
                    {
                        "type": "rich_text_section",
                        "elements": [
                            {"type": "text", "text": "success"},
                        ],
                    },
                    {
                        "type": "rich_text_list",
                        "style": "bullet",
                        "elements": [
                            {
                                "type": "rich_text_section",
                                "elements": [
                                    {"type": "text", "text": "Status: "},
                                    {"type": "text", "text": "connected"},
                                ],
                            },
                            {
                                "type": "rich_text_section",
                                "elements": [
                                    {"type": "text", "text": "IP: "},
                                    {"type": "text", "text": ip},
                                ],
                            },
                            {
                                "type": "rich_text_section",
                                "elements": [
                                    {"type": "text", "text": "Host: "},
                                    {"type": "text", "text": host},
                                ],
                            },
                        ],
                    },
                ],
            }
        ],
    )


# 自信のパブリックIPアドレスを取得する関数
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("", 1))
    ip = s.getsockname()[0]
    s.close()
    ip = str(ip)
    return ip


# 自信のホスト名を取得する関数
def get_hostname():
    hostname = socket.gethostname()
    return hostname
