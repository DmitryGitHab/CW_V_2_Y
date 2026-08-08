"""Клиент VK API: определение ID профиля и получение фотографий.

VK ограничивает частоту запросов и в ответ на превышение возвращает не
HTTP-ошибку, а обычный 200 с телом {"error": {"error_code": 6, ...}}.
Без отдельной обработки это выглядело бы как случайный сбой в середине
бэкапа. Здесь такая ошибка перехватывается и запрос повторяется с паузой.
"""

import logging
import time

import requests

logger = logging.getLogger(__name__)

VK_API_VERSION = "5.199"
VK_API_URL = "https://api.vk.com/method"

RATE_LIMIT_ERROR_CODE = 6
MAX_RETRIES = 5
RETRY_DELAY = 1.0  # секунды, растёт линейно с номером попытки


class VkApiError(RuntimeError):
    """Ошибка VK API, не связанная с превышением лимита частоты запросов."""


class VkClient:
    def __init__(self, access_token: str):
        self._token = access_token

    def _call(self, method: str, params: dict) -> dict:
        """Выполняет запрос к VK API с повтором при rate-limit ошибке."""
        request_params = {**params, "access_token": self._token, "v": VK_API_VERSION}

        for attempt in range(1, MAX_RETRIES + 1):
            response = requests.get(f"{VK_API_URL}/{method}", params=request_params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if "error" not in data:
                return data

            error = data["error"]
            if error.get("error_code") == RATE_LIMIT_ERROR_CODE and attempt < MAX_RETRIES:
                delay = RETRY_DELAY * attempt
                logger.warning(
                    "VK API: превышен лимит запросов (попытка %s/%s), пауза %.1fs",
                    attempt, MAX_RETRIES, delay,
                )
                time.sleep(delay)
                continue

            raise VkApiError(error.get("error_msg", "Unknown VK API error"))

        raise VkApiError("Превышено число попыток запроса к VK API")

    def resolve_profile_id(self, screen_name: str) -> int:
        """Определяет числовой ID профиля по короткому имени.

        Если на вход уже пришло число — возвращает его как есть, не делая
        лишний запрос к API.
        """
        if screen_name.isdigit():
            return int(screen_name)

        data = self._call("utils.resolveScreenName", {"screen_name": screen_name})
        if not data.get("response"):
            raise VkApiError(f"Не удалось найти профиль '{screen_name}'")
        return data["response"]["object_id"]

    def get_profile_photos(self, owner_id: int, count: int) -> list[dict]:
        """Возвращает сырые данные о фотографиях профиля (альбом 'profile')."""
        data = self._call(
            "photos.get",
            {"owner_id": owner_id, "album_id": "profile", "extended": 1, "count": count},
        )
        return data["response"]["items"][:count]
