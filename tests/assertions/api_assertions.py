import json
from typing import Iterable

import allure


def attach_response(response, name: str = "response"):
    try:
        payload = response.json()
        content = json.dumps(payload, ensure_ascii=False, indent=2)
        attachment_type = allure.attachment_type.JSON
    except Exception:
        content = response.text
        attachment_type = allure.attachment_type.TEXT

    allure.attach(content, name=name, attachment_type=attachment_type)


def assert_status(response, expected_status: int):
    attach_response(response)
    assert response.status_code == expected_status


def assert_json_has_keys(payload: dict, keys: Iterable[str]):
    for key in keys:
        assert key in payload
