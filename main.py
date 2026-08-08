"""Точка входа: интерактивный запуск бэкапа фотографий VK-профиля на Яндекс.Диск."""

from config import load_tokens
from services.backup import backup_profile_photos
from services.vk_client import VkClient
from services.yandex_disk import YandexDiskUploader


def main() -> None:
    tokens = load_tokens()
    profile = input("Введите screen_name или числовой ID профиля VK: ").strip()
    count = int(input("Сколько фото скачать: ").strip())

    vk = VkClient(tokens.vk)
    yandex = YandexDiskUploader(tokens.yandex)

    report = backup_profile_photos(vk, yandex, profile, count)
    print(f"Готово! Загружено {len(report)} фото. Отчёт сохранён в report.json")


if __name__ == "__main__":
    main()
