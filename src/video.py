import json
import os

from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')


class Video:
    def __init__(self, video_id: str) -> None:
        self.__video_id = video_id
        self.__key_api = api_key
        self.__video = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                        id=self.video_id
                                                        ).execute()
        self.__title: str = self.video['items'][0]['snippet']['title']
        self.__url = f"https://youtu.be/{self.video_id}"
        self.__view_count: int = self.video['items'][0]['statistics']['viewCount']
        self.__like_count: int = self.video['items'][0]['statistics']['likeCount']
        self.__comment_count: int = self.video['items'][0]['statistics']['commentCount']

    def __str__(self):
        return f'{self.title}'

    def print_info(self) -> None:
        print(json.dumps(self.video, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, file_name):
        with open(file_name, 'w') as outfile:
            json.dump(self.video, outfile)

    @property
    def video(self):
        return self.__video

    @property
    def video_id(self):
        return self.__video_id

    @property
    def title(self):
        return self.__title

    @property
    def url(self):
        return self.__url

    @property
    def like_count(self):
        return self.__like_count

    @property
    def view_count(self):
        return self.__view_count

    @property
    def comment_count(self):
        return self.__comment_count


class PLVideo(Video):
    def __init__(self, video_id: str, play_list_id: str):
        super().__init__(video_id)
        self.__play_list_id = play_list_id

    def __str__(self):
        return f'{self.title}'

    @property
    def play_list_id(self):
        return self.__play_list_id
