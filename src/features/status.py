from type.type import MentionEventHandlerArgs
from modules.bolt.reply import reply
import socket
import subprocess
import os


def handler(args: MentionEventHandlerArgs) -> None:
    global_ip = get_global_ip()
    local_ip = get_local_ip()
    host = get_hostname()
    git_commit_id = get_git_commit_id()
    port = "8081"
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
                                    {"type": "text", "text": "Version: "},
                                    {
                                        "type": "link",
                                        "url": f"https://github.com/Yoshida24/slackpi/commit/{git_commit_id}",
                                        "text": git_commit_id,
                                    },
                                ],
                            },
                            {
                                "type": "rich_text_section",
                                "elements": [
                                    {"type": "text", "text": "Host: "},
                                    {
                                        "type": "link",
                                        "url": f"https://{host}:{port}/",
                                        "text": host,
                                    },
                                ],
                            },
                            {
                                "type": "rich_text_section",
                                "elements": [
                                    {"type": "text", "text": "Local IP: "},
                                    {
                                        "type": "link",
                                        "url": f"https://{local_ip}:{port}/",
                                        "text": local_ip,
                                    },
                                ],
                            },
                            {
                                "type": "rich_text_section",
                                "elements": [
                                    {"type": "text", "text": "Global IP: "},
                                    {"type": "text", "text": global_ip},
                                ],
                            },
                        ],
                    },
                ],
            }
        ],
    )


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


def get_hostname():
    hostname = socket.gethostname()
    return hostname


def get_git_commit_id():
    dir = os.getcwd()
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=dir, stdout=subprocess.PIPE
    )
    return result.stdout.decode("utf-8").strip()[:7]
