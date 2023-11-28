import pandas as pd
from datetime import date
import requests
import json
import os

today = date.today()

def get_video_stats(youtube_api_key, similar_channels_list, number_results, quantile):

    # similar_channels_df = pd.read_csv("similar_channels.csv")
    # similar_channels_list = similar_channels_df['channels'].to_list()

    for channel_id in similar_channels_list:
        # get a list of latest videos of this channel
        video_info_url = f'https://www.googleapis.com/youtube/v3/search?key={youtube_api_key}&channelId={channel_id}&part=snippet,id&order=date&maxResults={number_results}'
        json_video_info = requests.get(video_info_url)
        video_data = json.loads(json_video_info.text)
        video_list = video_data.get('items')

        channel_video_stats = []

        for video in video_list:
            if video['id']['kind']=='youtube#video':
                snippet = video.get("snippet")
                video_title = snippet.get("title")
                video_pub_date = snippet.get("publishedAt")
                video_description = snippet.get("description")
                video_thumbnail = snippet.get("thumbnails").get('high').get('url')
                video_id = video.get('id').get('videoId')

                # get detailed information on these videos
                video_stats_url = f'https://www.googleapis.com/youtube/v3/videos?key={youtube_api_key}&id={video_id}&part=contentDetails%2Cstatistics&order=date&maxResults=10'
                video_stats_info = requests.get(video_stats_url)
                video_stats = json.loads(video_stats_info.text)

                video_statistics = video_stats['items'][0]
                video_view_count = video_statistics.get('statistics').get('viewCount')
                video_like_count = video_statistics.get('statistics').get('likeCount')
                video_comment_count = video_statistics.get('statistics').get('commentCount')
                video_fav_count = video_statistics.get('statistics').get('favoriteCount')
                video_duration = video_statistics.get('contentDetails').get('duration')
                video_type = video_statistics.get('contentDetails').get('projection')

                video_data = {
                "channel_id":channel_id,
                "video_id":video_id,
                "video_title":video_title,
                "video_pub_date":video_pub_date,
                "video_description":video_description,
                "video_thumbnail":video_thumbnail,
                "video_view_count":video_view_count,
                "video_like_count":video_like_count,
                "video_comment_count":video_comment_count,
                "video_fav_count":video_fav_count,
                "video_duration":video_duration,
                "video_type":video_type
                }

                channel_video_stats.append(video_data)

        channel_df = pd.DataFrame(channel_video_stats)
        channel_df['most_views'] = channel_df['video_view_count'].astype(int).quantile(quantile)
        channel_df['well_performers'] = channel_df['video_view_count'].astype(float)>channel_df['most_views']
        channel_df['video_pub_date'] = pd.to_datetime(channel_df['video_pub_date']).dt.date

        if not os.path.exists(f'results/{channel_id}'):
            os.mkdir(f'results/{channel_id}')
        channel_df.to_csv(f'results/{channel_id}/videos.csv')

        print(f'{channel_id} is done being analyzed.')

