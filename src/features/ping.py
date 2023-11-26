from type.type import MentionEventHandlerArgs
from modules.bolt.reply import reply
import socket


def handler(args: MentionEventHandlerArgs) -> None:
    global_ip = get_global_ip()
    local_ip = get_local_ip()
    host = get_hostname()
    reply(
        args.app,
        mention_body=args.event,
        blocks=[
            {
                "type": "rich_text",
                "elements": [
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
                                    {"type": "text", "text": "Local IP: "},
                                    {"type": "text", "text": local_ip},
                                ],
                            },
                            {
                                "type": "rich_text_section",
                                "elements": [
                                    {"type": "text", "text": "Global IP: "},
                                    {"type": "text", "text": global_ip},
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
def get_global_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("", 1))
    ip = s.getsockname()[0]
    s.close()
    ip = str(ip)

    import requests

    response = requests.get("https://api.ipify.org")
    ip = response.text  # 210.170.167.35
    return ip


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(("10.255.255.255", 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = "127.0.0.1"
    finally:
        s.close()
    return IP


print(get_local_ip())


# 自信のホスト名を取得する関数
def get_hostname():
    hostname = socket.gethostname()
    return hostname
