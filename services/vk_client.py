"""Клиент VK API: определение ID профиля и получение фотографий."""

import requests

VK_API_VERSION = "5.199"
VK_API_URL = "https://api.vk.com/method"


class VkClient:
    def __init__(self, access_token: str):
        self._token = access_token

    def resolve_profile_id(self, screen_name: str) -> int:
        """Определяет числовой ID профиля по короткому имени.

        Если на вход уже пришло число — возвращает его как есть, не делая
        лишний запрос к API.
        """
        if screen_name.isdigit():
            return int(screen_name)

        response = requests.get(
            f"{VK_API_URL}/utils.resolveScreenName",
            params={
                "access_token": self._token,
                "v": VK_API_VERSION,
                "screen_name": screen_name,
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        if not data.get("response"):
            raise ValueError(f"Не удалось найти профиль '{screen_name}'")
        return data["response"]["object_id"]

    def get_profile_photos(self, owner_id: int, count: int) -> list[dict]:
        """Возвращает сырые данные о фотографиях профиля (альбом 'profile').

        В отличие от исходной версии, count реально передаётся в запрос —
        раньше он использовался только для нарезки ответа по индексам,
        без ограничения на стороне VK API, что могло привести к IndexError,
        если у профиля фото меньше, чем запрошено.
        """
        response = requests.get(
            f"{VK_API_URL}/photos.get",
            params={
                "owner_id": owner_id,
                "album_id": "profile",
                "extended": 1,
                "count": count,
                "v": VK_API_VERSION,
                "access_token": self._token,
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        if "error" in data:
            raise RuntimeError(f"VK API error: {data['error'].get('error_msg')}")
        return data["response"]["items"][:count]
