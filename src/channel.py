import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key = os.getenv('YT_API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется по id канала. Дальше все данные будут подтягиваться по API."""
        self.channel = self.get_service().channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = self.channel["items"][0]["snippet"]["title"]
        self.description = self.channel["items"][0]["snippet"]["description"]
        self.video_count = int(self.channel["items"][0]["statistics"]["videoCount"])
        self.subscribers = int(self.channel["items"][0]["statistics"]["subscriberCount"])
        self.url = f'https://www.youtube.com/channel/{channel_id}'

    def __str__(self):
        return f'{self.title} {self.url}'

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    def to_json(self, file_name: str) -> None:
        """
        Сохраняет в файл значения атрибутов экземпляра `Channel`
        """
        file_name = self.title
        data = {"channel_id": self.channel_id,
                "title": self.title,
                "description": self.description,
                "video_count": self.video_count,
                "subscribers": self.subscribers,
                "url": self.url
                }
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def __add__(self, other):
        """Сложение числа подписчиков двух каналов"""
        return self.subscribers + other.subscribers

    def __sub__(self, other):
        """Вычитание числа подписчиков одного канала из числа подписчиков другого канала"""
        return self.subscribers - other.subscribers

    def __gt__(self, other):
        """Метод сравнения больше: одно число > другого. Возвращает булевое значение"""
        return self.subscribers > other.subscribers

    def __ge__(self, other):
        """Метод сравнения: одно число >= другого. Возвращает булевое значение"""
        return self.subscribers >= other.subscribers

    def __lt__(self, other):
        """Метод сравнения меньше: одно число < другого. Возвращает булевое значение"""
        return self.subscribers < other.subscribers

    def __le__(self, other):
        """Метод сравнения: одно число <= другого. Возвращает булевое значение"""
        return self.subscribers <= other.subscribers
