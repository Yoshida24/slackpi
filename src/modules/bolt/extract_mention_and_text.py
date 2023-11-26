import re
from typing import TypedDict

MentionText = TypedDict(
    "MentionText",
    {
        "mention": str | None,
        "text": str,
    },
)


def extract_mention_and_text(input_string: str) -> MentionText:
    # 正規表現を使用してメンションとテキストを抽出
    mention_pattern = r"<@([^>]+)>"
    mention_match = re.search(mention_pattern, input_string)

    if mention_match:
        mention = "@" + mention_match.group(1)
        text = re.sub(mention_pattern, "", input_string).strip()
    else:
        mention = None
        text = input_string.strip()

    result: MentionText = {"mention": mention, "text": text}

    return result
