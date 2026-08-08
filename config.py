"""Загрузка токенов VK и Yandex.Disk.

Формат token.txt (файл не пушится в git, см. .gitignore):
    yandex: XXX
    vk: YYY

Если файла нет или он неполный — токены запрашиваются вручную.
"""

from dataclasses import dataclass
from pathlib import Path

TOKEN_FILE = Path("token.txt")


@dataclass(frozen=True)
class Tokens:
    yandex: str
    vk: str


def load_tokens() -> Tokens:
    if TOKEN_FILE.exists():
        values: dict[str, str] = {}
        for line in TOKEN_FILE.read_text(encoding="utf-8").splitlines():
            if ":" not in line:
                continue
            key, _, value = line.partition(":")
            values[key.strip().lower()] = value.strip()

        if "yandex" in values and "vk" in values:
            return Tokens(yandex=values["yandex"], vk=values["vk"])

    print("token.txt не найден или неполный — введите токены вручную.")
    yandex = input("Yandex.Disk OAuth-токен: ").strip()
    vk = input("VK access_token: ").strip()
    return Tokens(yandex=yandex, vk=vk)
