# botからのメッセージか判定
def is_message_from_bot(message: dict) -> bool:
    return "bot_id" in message
