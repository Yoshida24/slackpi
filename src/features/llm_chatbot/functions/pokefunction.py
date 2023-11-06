import json

import requests


def fetch_pokemon_data(name: str, **kwargs):
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = {
            "wight": response.json()["weight"] * 0.1,
            "height": response.json()["height"] * 0.1,
        }
        return {"message": json.dumps(data), "file": None}
    else:
        return {"message": "not found.", "file": None}


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
