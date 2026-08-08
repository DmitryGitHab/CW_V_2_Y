"""Точка входа: бэкап фотографий VK-профиля на Яндекс.Диск.

Поддерживает и аргументы командной строки (для запуска по cron/из
скриптов), и интерактивный ввод, если аргументы не переданы.
"""

import argparse
import logging

from config import load_tokens
from services.backup import backup_profile_photos
from services.vk_client import VkClient
from services.yandex_disk import YandexDiskUploader

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Бэкап фотографий VK-профиля на Яндекс.Диск")
    parser.add_argument("--profile", help="screen_name или числовой ID профиля VK")
    parser.add_argument("--count", type=int, help="Сколько фото скачать")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tokens = load_tokens()

    profile = args.profile or input("Введите screen_name или числовой ID профиля VK: ").strip()
    count = args.count or int(input("Сколько фото скачать: ").strip())

    vk = VkClient(tokens.vk)
    yandex = YandexDiskUploader(tokens.yandex)

    report = backup_profile_photos(vk, yandex, profile, count)

    total_likes = sum(item["likes"] for item in report)
    logger.info("Готово: загружено %s фото, суммарно %s лайков", len(report), total_likes)
    logger.info("Подробный отчёт сохранён в report.json")


if __name__ == "__main__":
    main()
