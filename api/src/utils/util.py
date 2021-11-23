from typing import Any


def get_dict_value(dic: dict, key: str, default_value: Any = None) -> Any:
    if key in dic:
        return dic[key]

    if default_value is not None:
        return default_value

    return ""
