import json
import os

from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.__key_api = api_key
        self.__channel = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.__title = self.channel["items"][0]["snippet"]["title"]
        self.__description = self.channel["items"][0]["snippet"]["description"]
        self.__url = f"https://www.youtube.com/channel/{self.channel_id}"
        self.__subscriber_count = int(self.channel["items"][0]["statistics"]["subscriberCount"])
        self.__video_count = int(self.channel["items"][0]["statistics"]["videoCount"])
        self.__view_count = int(self.channel["items"][0]["statistics"]["viewCount"])

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        return self.subscriber_count - other.subscriber_count

    def __it__(self, other):
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        return self.subscriber_count <= other.subscriber_count

    def __gt__(self, other):
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        return self.subscriber_count >= other.subscriber_count

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.get_service, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, file_name):
        with open(file_name, 'w') as outfile:
            json.dump(self.channel, outfile)

    @property
    def channel(self):
        return self.__channel

    @property
    def channel_id(self):
        return self.__channel_id

    @property
    def title(self):
        return self.__title

    @property
    def description(self):
        return self.__description

    @property
    def url(self):
        return self.__url

    @property
    def subscriber_count(self):
        return self.__subscriber_count

    @property
    def video_count(self):
        return self.__video_count

    @property
    def view_count(self):
        return self.__view_count

    def requests(self):
        print(self.channel.response.request.url)
