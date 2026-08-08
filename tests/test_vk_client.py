"""Тесты для VkClient."""

from unittest.mock import MagicMock, patch

import pytest

from services.vk_client import VkApiError, VkClient


def _mock_response(json_data: dict, status_code: int = 200) -> MagicMock:
    mock = MagicMock()
    mock.status_code = status_code
    mock.json.return_value = json_data
    mock.raise_for_status = MagicMock()
    return mock


@patch("services.vk_client.requests.get")
def test_resolve_profile_id_numeric_skips_api_call(mock_get):
    client = VkClient("token")
    assert client.resolve_profile_id("12345") == 12345
    mock_get.assert_not_called()


@patch("services.vk_client.requests.get")
def test_resolve_profile_id_by_screen_name(mock_get):
    mock_get.return_value = _mock_response({"response": {"object_id": 999}})
    client = VkClient("token")
    assert client.resolve_profile_id("durov") == 999


@patch("services.vk_client.requests.get")
def test_resolve_profile_id_not_found_raises(mock_get):
    mock_get.return_value = _mock_response({"response": []})
    client = VkClient("token")
    with pytest.raises(VkApiError):
        client.resolve_profile_id("no_such_user")


@patch("services.vk_client.time.sleep", return_value=None)
@patch("services.vk_client.requests.get")
def test_rate_limit_retries_then_succeeds(mock_get, mock_sleep):
    rate_limited = _mock_response({"error": {"error_code": 6, "error_msg": "Too many requests"}})
    success = _mock_response({"response": {"items": [{"id": 1}]}})
    mock_get.side_effect = [rate_limited, success]

    client = VkClient("token")
    data = client._call("photos.get", {})

    assert data["response"]["items"] == [{"id": 1}]
    assert mock_get.call_count == 2
    mock_sleep.assert_called_once()


@patch("services.vk_client.requests.get")
def test_non_rate_limit_error_raises_immediately(mock_get):
    mock_get.return_value = _mock_response(
        {"error": {"error_code": 5, "error_msg": "Invalid access token"}}
    )
    client = VkClient("token")
    with pytest.raises(VkApiError, match="Invalid access token"):
        client._call("photos.get", {})
    assert mock_get.call_count == 1


@patch("services.vk_client.requests.get")
def test_get_profile_photos_limits_to_count(mock_get):
    items = [{"id": i} for i in range(5)]
    mock_get.return_value = _mock_response({"response": {"items": items}})
    client = VkClient("token")
    result = client.get_profile_photos(owner_id=1, count=3)
    assert len(result) == 3
