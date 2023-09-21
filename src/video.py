import os
from googleapiclient.discovery import build


class Video:
    api_key = os.getenv('YT_API_KEY')

    def __init__(self, video_id: str):
        self.video_id = video_id
        try:
            self.video = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                          id=video_id).execute()
            self.title = self.video['items'][0]['snippet']['title']
            self.view_count = self.video['items'][0]['statistics']['viewCount']
            self.video_url = f"https://www.youtube.com/watch?v={video_id}"
            self.like_count = self.video['items'][0]['statistics']['likeCount']
        except IndexError:
            print("Введен некорректрый ID видео.")
            self.video = None
            self.title = None
            self.view_count = None
            self.video_url = None
            self.like_count = None

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)

    def __str__(self):
        return f'{self.title_video}'


class PLVideo(Video):

    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.playlist_id = playlist_id
