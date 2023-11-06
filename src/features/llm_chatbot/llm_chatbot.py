from type.type import MentionEventHandlerArgs
from modules.bolt.update_message import update_message
from modules.bolt.reply import reply
from modules.bolt.upload_file import upload_file
import openai
from typing import cast
import os
import json

from .functions.pokefunction import fetch_pokemon_data, function
from .functions.screenshot import take_screenshot, screenshot_function
from typing import Callable
import time

import logging
from dataclasses import asdict

logger = logging.getLogger(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

model_name = "gpt-3.5-turbo"
temperature = 0.9
max_tokens = 2048
system_msg = "Friendly and helpful AI assistant at Choimirai School,\
    which is powerd by OpenAI's latest AI model.\
    Her name is Riley."


def response(
    messages: list[dict],
    present_stream_response: Callable[[str], None],
    args: MentionEventHandlerArgs,
    message_ts: str,
) -> dict:
    function_response_file = None
    functions = [function, screenshot_function]

    first_response = stream_response(
        openai.ChatCompletion.create(
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=1,
            messages=messages,
            functions=functions,
            # functions=[screenshot_function],
            function_call="auto",
            stream=True,
        ),
        present_stream_response,
    )

    first_message = cast(dict, first_response)["choices"][0]["message"]

    # limit = 2
    # for i in range(limit):
    if first_message.get("function_call"):
        """
        function_call が実行された場合
        """
        function_name = first_message["function_call"]["name"]
        arguments = json.loads(first_message["function_call"]["arguments"])
        function_response = None

        # 関数の実行
        # function_response = fetch_pokemon_data(**arguments)
        for f in functions:
            if function_name == f["name"]:
                if function_name == "take_screenshot":
                    selected_function = take_screenshot
                elif function_name == "fetch_pokemon_data":
                    selected_function = fetch_pokemon_data
                else:
                    raise Exception("function not found")

                function_response = selected_function(**arguments)
                function_response_msg = function_response["message"]
                function_response_file = function_response["file"]
                logger.info(f"function_name={function_name} arguments={arguments}")
                logger.info(
                    f"function_response_msg={function_response_msg} function_response_file={function_response_file}"
                )

        # 関数実行結果を使ってもう一度質問
        second_response = stream_response(
            openai.ChatCompletion.create(
                model=model_name,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=1,
                messages=[message for message in messages]
                + [first_message]
                + [
                    {
                        "role": "function",
                        "name": function_name,
                        "content": function_response_msg,
                    }
                ],
                stream=True,
            ),
            present_stream_response,
        )

        response = second_response
    else:
        response = first_response

    logger.info(response)

    if function_response_file is not None:
        upload_file(
            app=args.app,
            mention_body=args.event,
            file=function_response_file,
            thread_ts=message_ts,
        )
    return {
        "content": response["choices"][0]["message"]["content"],
        "file": function_response_file,
    }


def present_stream_response_clojure(args: MentionEventHandlerArgs, message_ts: str):
    def present_stream_response(text: str | None):
        if text is None or text == "":
            return
        update_message(
            app=args.app,
            channel=args.event.event.channel,
            ts=message_ts,
            text=text,
        )

    return present_stream_response


def stream_response(
    streaming_response,
    streaming: Callable[[str], None],
    update_interval=0.5,
):
    chat_compilation_content = ""
    function_calling_argument = ""
    function_calling_name = ""
    last_update = time.time()

    for chunk in streaming_response:
        is_function_call_in_progress = "function_call" in chunk.choices[0].delta
        is_function_call_finished = any(
            choice.get("finish_reason") == "function_call"
            for choice in chunk.get("choices", [])
        )
        is_function_call = is_function_call_in_progress or is_function_call_finished
        if is_function_call:
            if is_function_call_finished:
                return {
                    "choices": [
                        {
                            "message": {
                                "content": None,
                                "role": "assistant",
                                "function_call": {
                                    "name": function_calling_name,
                                    "arguments": function_calling_argument,
                                },
                            }
                        }
                    ],
                    "usage": None,
                }
            elif is_function_call_in_progress:
                if "name" in chunk.choices[0].delta.function_call:
                    function_calling_name = (
                        function_calling_name
                        + chunk.choices[0].delta.function_call.name
                    )
                if "arguments" in chunk.choices[0].delta.function_call:
                    function_calling_argument = (
                        function_calling_argument
                        + chunk.choices[0].delta.function_call.arguments
                    )
        else:
            is_text_compilation_finished = any(
                choice.get("finish_reason") == "stop"
                for choice in chunk.get("choices", [])
            )
            if is_text_compilation_finished:
                streaming(chat_compilation_content)
                return {
                    "choices": [
                        {
                            "message": {
                                "content": chat_compilation_content,
                                "role": "assistant",
                            }
                        }
                    ],
                    "usage": None,
                }
            else:
                delta = chunk.choices[0].delta.content
                chat_compilation_content = chat_compilation_content + delta
                if time.time() - last_update > update_interval:
                    last_update = time.time()
                    streaming(chat_compilation_content)
    raise Exception("not found")


def handler(args: MentionEventHandlerArgs) -> None:
    res = reply(
        app=args.app,
        mention_body=args.event,
        text="...",
    )
    present_stream_response = present_stream_response_clojure(args, res["ts"])
    messages = []
    messages.append({"role": "system", "content": system_msg})
    messages.append({"role": "user", "content": args.event.event.text})
    response(
        messages=messages,
        present_stream_response=present_stream_response,
        args=args,
        message_ts=res["ts"],
    )
