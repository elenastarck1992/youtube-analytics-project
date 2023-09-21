import json
import os
from googleapiclient.discovery import build
import datetime, isodate


class PlayList():
    api_key = os.getenv('YT_API_KEY')

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.playlist = self.get_service().playlists().list(id=playlist_id,
                                               part='contentDetails, snippet',
                                               ).execute()
        self.title = self.playlist['items'][0]['snippet']['title']
        self.url = "https://www.youtube.com/playlist?list=" + self.playlist['items'][0]['id']
        # получаем данные по плейлистам
        self.playlist_videos = self.get_service().playlistItems().list(playlistId=playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        # получить все id видеороликов из плейлиста
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        # получить все данные по видеороликам
        self.video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()


    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)

    @property
    def total_duration(self):
        """Получает длительность плейлиста"""
        total_duration = datetime.timedelta()
        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def show_best_video(self):
        max_likes = 0
        video_id = ''
        for video in self.video_response['items']:
            count_likes = int(video['statistics']['likeCount'])
            if max_likes < count_likes:
                max_likes = count_likes
                video_id = video['id']
        return f'https://youtu.be/{video_id}'

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.playlist, indent=2, ensure_ascii=False))
