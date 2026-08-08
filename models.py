"""Модель данных для фотографии VK.

Раньше объекты хранились как переменные в globals() с именами вида
'photo_0', 'photo_1', а доступ к ним шёл через eval("photo_0"). Это
взлом на пустом месте: обычный список объектов даёт то же самое, но
безопасно, читаемо и с поддержкой автодополнения/тайпчекера.
"""

from dataclasses import dataclass


@dataclass
class VkPhoto:
    url: str
    size_type: str
    likes: int
    upload_date: int  # unix timestamp

    @property
    def file_name(self) -> str:
        return f"{self.likes}.jpg"

    @classmethod
    def from_api_item(cls, item: dict) -> "VkPhoto":
        """Строит VkPhoto из одного элемента ответа VK API photos.get.

        Берём последний (самый большой) размер из item['sizes'] — так же,
        как было в исходной версии.
        """
        largest_size = item["sizes"][-1]
        return cls(
            url=largest_size["url"],
            size_type=largest_size["type"],
            likes=item["likes"]["count"],
            upload_date=item["date"],
        )
