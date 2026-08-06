from __future__ import annotations

import json
from typing import Callable


def process_json(
    json_str: str,
    required_keys: list[str] | None = None,
    tokens: list[str] | None = None,
    callback: Callable[[str, str], None] | None = None,
) -> None:
    if not json_str or not required_keys or not tokens or not callback:
        return
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError:
        return

    for key in required_keys:
        if key in data and isinstance(data[key], str):
            value = data[key]
            words = [word.lower() for word in value.split()]

            for token in tokens:
                normalized_token = token.lower()
                if normalized_token in words:
                    callback(key, token)
