from googleapiclient.discovery import build
import re

api_key = 'AIzaSyDn9ONJ33uwfoCL_02f0-3y-wSTqDBuC5s'


def get_video_comments(video_id):
    comments = []

    youtube = build('youtube', 'v3',
                    developerKey=api_key)

    video_response = youtube.commentThreads().list(
        part='snippet,replies',
        videoId=video_id,
    ).execute()

    # Ограничитель на количество страниц комментариев (для предотвращения превышения квоты)
    max_pages = 2
    act_page = 0

    while video_response and act_page < max_pages:
        for item in video_response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            cleaned_comment = re.sub(r"<[^>]+>", "", comment, flags=re.S)
            comments.append(cleaned_comment)

            reply_count = item['snippet']['totalReplyCount']

            if reply_count > 0:

                for reply in item['replies']['comments']:
                    reply = reply['snippet']['textDisplay']

                    comments.append(reply)

        if 'nextPageToken' in video_response:
            video_response = youtube.commentThreads().list(
                part='snippet,replies',
                videoId=video_id
            ).execute()

            act_page += 1
        else:
            break

    return comments

