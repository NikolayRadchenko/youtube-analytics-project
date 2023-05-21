import json
import os

from datetime import timedelta
import isodate
from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')


class PlayList:

    def __init__(self, playlist_id: str) -> None:
        self.__playlist_id = playlist_id
        self.__key_api = api_key
        self.__playlist_videos = self.get_service().playlistItems().list(playlistId=playlist_id,
                                                                         part='contentDetails',
                                                                         maxResults=50,
                                                                         ).execute()
        self.__video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.__video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                                 id=','.join(self.video_ids)
                                                                 ).execute()
        self.__playlist_videos = self.get_service().playlists().list(id=playlist_id,
                                                                     part='snippet',
                                                                     maxResults=50,
                                                                     ).execute()
        self.__title = self.playlist_videos['items'][0]['snippet']['title']
        self.__url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    def print_info(self) -> None:
        print(json.dumps(self.playlist_videos, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=api_key)

    @property
    def playlist_id(self):
        return self.__playlist_id

    @property
    def title(self):
        return self.__title

    @property
    def url(self):
        return self.__url

    @property
    def playlist_videos(self):
        return self.__playlist_videos

    @property
    def video_ids(self):
        return self.__video_ids

    @property
    def video_response(self):
        return self.__video_response

    @property
    def total_duration(self):
        total_duration = timedelta()
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def show_best_video(self):
        like_count = 0
        video_id = ''
        for video in self.video_response['items']:
            if int(video["statistics"]["likeCount"]) > like_count:
                like_count = int(video["statistics"]["likeCount"])
                video_id = video["id"]
        return f"https://youtu.be/{video_id}"
