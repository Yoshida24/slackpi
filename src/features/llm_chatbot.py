from type.type import MentionEventHandlerArgs
from modules.bolt.reply import reply
import openai
from typing import cast
import os

import logging

logger = logging.getLogger(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")


model_name = "gpt-3.5-turbo"
temperature = 0.9
max_tokens = 2048
system_msg = "Friendly and helpful AI assistant at Choimirai School,\
    which is powerd by OpenAI's latest AI model.\
    Her name is Riley."


def response(messages: list[dict]) -> str:
    first_response = openai.ChatCompletion.create(
        model=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=1,
        messages=messages,
        # functions=functions,
        # function_call="auto",
        stream=False,
    )

    firse_message = cast(dict, first_response)["choices"][0]["message"]

    logger.info(response)
    return firse_message["content"]


def handler(args: MentionEventHandlerArgs) -> None:
    messages = []
    messages.append({"role": "system", "content": system_msg})
    messages.append({"role": "user", "content": args.event.event.text})
    res = response(messages)
    reply(
        args.app,
        mention_body=args.event,
        text=f"<@{args.event.event.user}>\n{res} ",
    )
