"""Оркестрация процесса бэкапа: VK → Yandex.Disk + JSON-отчёт."""

import datetime
import json
from pathlib import Path

from tqdm import tqdm

from models import VkPhoto
from services.vk_client import VkClient
from services.yandex_disk import YandexDiskUploader

REPORT_FILE = Path("report.json")


def _unique_file_name(photo: VkPhoto, used_names: set[str]) -> str:
    """Имя файла — количество лайков. Если уже встречалось фото с таким же
    числом лайков, добавляет дату загрузки, чтобы не перезаписать файл."""
    name = photo.file_name
    if name not in used_names:
        used_names.add(name)
        return name

    date_str = datetime.date.fromtimestamp(photo.upload_date).strftime("%Y-%m-%d")
    name = f"{photo.likes}_{date_str}.jpg"
    used_names.add(name)
    return name


def backup_profile_photos(
    vk: VkClient, yandex: YandexDiskUploader, profile: str, count: int
) -> list[dict]:
    profile_id = vk.resolve_profile_id(profile)
    raw_items = vk.get_profile_photos(profile_id, count)
    photos = [VkPhoto.from_api_item(item) for item in raw_items]

    folder = f"id_{profile_id}"
    yandex.create_folder(folder)

    used_names: set[str] = set()
    report = []
    for photo in tqdm(photos, desc="Загрузка на Яндекс.Диск"):
        file_name = _unique_file_name(photo, used_names)
        yandex.upload_from_url(photo.url, f"{folder}/{file_name}")
        report.append({"file_name": file_name, "size": photo.size_type, "likes": photo.likes})

    REPORT_FILE.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report
