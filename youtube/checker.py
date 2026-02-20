import logging
import sqlite3
from googleapiclient.discovery import build
from config import YOUTUBE_API_KEY, YOUTUBE_CHANNEL_ID, DB_FILE, PHRASES

logger = logging.getLogger(__name__)

def _get_last_video_id():
    with sqlite3.connect(DB_FILE) as conn:
        row = conn.execute(
            "SELECT value FROM config WHERE key='last_video_id'"
        ).fetchone()
        return row[0] if row else ""

def _set_last_video_id(video_id: str):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            "UPDATE config SET value=? WHERE key='last_video_id'",
            (video_id,)
        )

def check_for_new_videos():
    logger.info("Checking YouTube for new videos")

    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    channels_response = youtube.channels().list(part='contentDetails', id=YOUTUBE_CHANNEL_ID).execute()
    uploads_playlist_id = channels_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    playlist_response = youtube.playlistItems().list(part='snippet', playlistId=uploads_playlist_id, maxResults=5).execute()
    items = playlist_response['items']

    last_id = _get_last_video_id()
    new_videos = []

    for item in sorted(items, key=lambda x: x['snippet']['publishedAt'], reverse=True):
        video_id = item['snippet']['resourceId']['videoId']

        if video_id == last_id:
            break

    title = item['snippet']['title'].lower()

    matches = any(phrase.lower() in title for phrase in PHRASES)

    if matches:
        new_videos.append({
            'title': item['snippet']['title'],
            'url': f"https://www.youtube.com/watch?v={video_id}"
        })

    if items:
        latest_id = items[0]['snippet']['resourceId']['videoId']
        _set_last_video_id(latest_id)

    logger.info("Found %d new videos", len(new_videos))
    return new_videos

# def check_for_new_videos():
#     logger.info("Checking YouTube for new videos")
#
#     youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
#
#     # Get upload playlist
#     channels_response = youtube.channels().list(
#         part='contentDetails',
#         id=YOUTUBE_CHANNEL_ID
#     ).execute()
#     uploads_playlist_id = channels_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
#
#     # ────────────────────────────────────────────────
#     # Decide time filter for testing
#     import os
#     from datetime import datetime, timedelta, timezone
#
#     test_24h = os.getenv('TEST_LAST_24H', 'false').lower() == 'true'
#
#     if test_24h:
#         # Only videos from last 24 hours
#         published_after = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()
#         # We'll use search instead of playlistItems for date filtering
#         print("TEST MODE: Looking only for videos published in last 24 hours")
#
#         search_response = youtube.search().list(
#             part='id,snippet',
#             channelId=YOUTUBE_CHANNEL_ID,
#             order='date',
#             type='video',
#             publishedAfter=published_after,
#             maxResults=10
#         ).execute()
#
#         items = search_response.get('items', [])
#
#     else:
#         # Normal mode: recent uploads via playlist
#         playlist_response = youtube.playlistItems().list(
#             part='snippet',
#             playlistId=uploads_playlist_id,
#             maxResults=10
#         ).execute()
#         items = playlist_response.get('items', [])
#     # ────────────────────────────────────────────────
#
#     last_id = _get_last_video_id()
#     new_videos = []
#
#     # Sort by publish time descending (newest first)
#     sorted_items = sorted(
#         items,
#         key=lambda x: x['snippet']['publishedAt'],
#         reverse=True
#     )
#
#     for item in sorted_items:
#         video_id = item['id']['videoId'] if test_24h else item['snippet']['resourceId']['videoId']
#
#         # Skip already processed videos (unless in test mode we might want to force notify)
#         if not test_24h and video_id == last_id:
#             break
#
#         title = item['snippet']['title'].lower()
#
#         matches = any(phrase.lower() in title for phrase in PHRASES)
#
#         if matches:
#             new_videos.append({
#                 'title': item['snippet']['title'],
#                 'url': f"https://www.youtube.com/watch?v={video_id}"
#             })
#
#     # Only update last_video_id in normal mode
#     if not test_24h and sorted_items:
#         latest_id = sorted_items[0]['snippet']['resourceId']['videoId']
#         _set_last_video_id(latest_id)
#
#     return new_videos