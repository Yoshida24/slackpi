from type.type import MentionEventHandlerArgs
from modules.bolt.reply import reply
import openai
from typing import cast
import os
import json
from .pokefunction import fetch_pokemon_data, function

import logging
from dataclasses import asdict

logger = logging.getLogger(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

###aaa

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
        functions=[function],
        function_call="auto",
        stream=False,
    )

    firse_message = cast(dict, first_response)["choices"][0]["message"]

    limit = 2
    for i in range(limit):
        if firse_message.get("function_call"):
            """
            function_call が実行された場合
            """
            function_name = (
                "fetch_pokemon_data"  # firse_message["function_call"]["name"]
            )
            arguments = json.loads(firse_message["function_call"]["arguments"])
            function_response = None

            # 関数の実行
            function_response = fetch_pokemon_data(**arguments)
            # for f_name, f_impl in function_calling_def.use_functions.items():
            #     if function_name == f_name:
            #         logger.info(f"function_name={function_name} arguments={arguments}")
            #         function_response = f_impl(**arguments)
            #         logger.info(function_response)

            # 関数実行結果を使ってもう一度質問
            second_response = openai.ChatCompletion.create(
                model=model_name,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=1,
                messages=[messages for message in messages]
                + [firse_message]
                + [
                    {
                        "role": "function",
                        "name": function_name,
                        "content": function_response,
                    }
                ],
                stream=True,
            )

            response = second_response
        else:
            response = first_response

        logger.info(response)
    return firse_message["content"]


# def stream_response():
#     chat_compilation_content = ""
#     function_calling_argument = ""
#     function_calling_name = ""

#     for chunk in streaming_response:
#         is_function_call_in_progress = "function_call" in chunk.choices[0].delta
#         is_function_call_finished = any(
#             choice.get("finish_reason") == "function_call"
#             for choice in chunk.get("choices", [])
#         )
#         is_function_call = is_function_call_in_progress or is_function_call_finished
#         if is_function_call:
#             if is_function_call_finished:
#                 return {
#                     "choices": [
#                         {
#                             "message": {
#                                 "content": None,
#                                 "role": "assistant",
#                                 "function_call": {
#                                     "name": function_calling_name,
#                                     "arguments": function_calling_argument,
#                                 },
#                             }
#                         }
#                     ],
#                     "usage": None,
#                 }
#             elif is_function_call_in_progress:
#                 if "name" in chunk.choices[0].delta.function_call:
#                     function_calling_name = (
#                         function_calling_name
#                         + chunk.choices[0].delta.function_call.name
#                     )
#                 if "arguments" in chunk.choices[0].delta.function_call:
#                     function_calling_argument = (
#                         function_calling_argument
#                         + chunk.choices[0].delta.function_call.arguments
#                     )
#         else:
#             is_text_compilation_finished = any(
#                 choice.get("finish_reason") == "stop"
#                 for choice in chunk.get("choices", [])
#             )
#             if is_text_compilation_finished:
#                 message_post.finish()
#                 return {
#                     "choices": [
#                         {
#                             "message": {
#                                 "content": chat_compilation_content,
#                                 "role": "assistant",
#                             }
#                         }
#                     ],
#                     "usage": None,
#                 }
#             else:
#                 delta = chunk.choices[0].delta.content
#                 chat_compilation_content = chat_compilation_content + delta
#                 message_post.add_text(delta)
#     raise Exception("not found")


# text = openai_response["choices"][0]["message"]["content"]


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
