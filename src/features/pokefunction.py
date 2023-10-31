from __future__ import annotations

import json

import requests


def fetch_pokemon_data(name: str, **kwargs):
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = {
            "wight": response.json()["weight"],
            "height": response.json()["height"],
        }
        return json.dumps(data)
    else:
        return None


function = {
    "name": "fetch_pokemon_data",
    "description": "Fetch pokemon data by pokemon name.",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "Pokemon name, e.g. pikachu",
            },
        },
        "required": ["name"],
    },
}
