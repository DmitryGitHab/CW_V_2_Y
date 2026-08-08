"""Клиент Yandex.Disk REST API: создание папки и загрузка файлов по URL."""

import requests

from services.retry import retry

YANDEX_API_URL = "https://cloud-api.yandex.net/v1/disk"


class YandexDiskUploader:
    def __init__(self, token: str):
        self._headers = {
            "Content-Type": "application/json",
            "Authorization": f"OAuth {token}",
        }

    def create_folder(self, path: str) -> None:
        """Создаёт папку на Яндекс.Диске.

        Раньше проверка выглядела как
            if response.status_code == 200 or 201 or 202:
        что в Python эквивалентно (status_code == 200) or 201 or 202 —
        а 201 truthy, поэтому условие было ВСЕГДА истинным независимо от
        реального ответа сервера. Здесь — явная проверка через `in`.
        """
        response = requests.put(
            f"{YANDEX_API_URL}/resources",
            headers=self._headers,
            params={"path": path},
            timeout=10,
        )
        # 409 — папка уже существует, это не ошибка в нашем сценарии
        if response.status_code not in (200, 201, 409):
            response.raise_for_status()

    @retry(times=3, base_delay=1.5, exceptions=(requests.exceptions.RequestException,))
    def upload_from_url(self, source_url: str, destination_path: str) -> None:
        """Загружает файл по URL. При сетевом сбое повторяет попытку до 3 раз."""
        response = requests.post(
            f"{YANDEX_API_URL}/resources/upload",
            headers=self._headers,
            params={"path": destination_path, "url": source_url},
            timeout=10,
        )
        response.raise_for_status()
