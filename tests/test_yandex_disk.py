"""Тесты для YandexDiskUploader."""

from unittest.mock import MagicMock, patch

import requests

from services.yandex_disk import YandexDiskUploader


def _mock_response(status_code: int = 200) -> MagicMock:
    mock = MagicMock()
    mock.status_code = status_code
    mock.raise_for_status = MagicMock()
    return mock


@patch("services.yandex_disk.requests.put")
def test_create_folder_success(mock_put):
    mock_put.return_value = _mock_response(201)
    uploader = YandexDiskUploader("token")
    uploader.create_folder("id_1")
    mock_put.assert_called_once()


@patch("services.yandex_disk.requests.put")
def test_create_folder_already_exists_is_not_an_error(mock_put):
    mock_put.return_value = _mock_response(409)
    uploader = YandexDiskUploader("token")
    uploader.create_folder("id_1")  # не должно бросить исключение


@patch("services.retry.time.sleep", return_value=None)
@patch("services.yandex_disk.requests.post")
def test_upload_retries_on_network_error_then_succeeds(mock_post, mock_sleep):
    mock_post.side_effect = [
        requests.exceptions.ConnectionError("boom"),
        _mock_response(201),
    ]
    uploader = YandexDiskUploader("token")
    uploader.upload_from_url("http://example.com/photo.jpg", "id_1/100.jpg")

    assert mock_post.call_count == 2
    mock_sleep.assert_called_once()


@patch("services.retry.time.sleep", return_value=None)
@patch("services.yandex_disk.requests.post")
def test_upload_gives_up_after_max_retries(mock_post, mock_sleep):
    mock_post.side_effect = requests.exceptions.ConnectionError("boom")
    uploader = YandexDiskUploader("token")

    try:
        uploader.upload_from_url("http://example.com/photo.jpg", "id_1/100.jpg")
        assert False, "ожидалось исключение ConnectionError"
    except requests.exceptions.ConnectionError:
        pass

    assert mock_post.call_count == 3  # times=3 в декораторе retry
