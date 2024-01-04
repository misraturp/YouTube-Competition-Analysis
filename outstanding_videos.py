import os
from datetime import date
import pandas as pd

def get_outstanding_videos(threshold, all_videos_df, quantile):

    # similar_channels_df = pd.read_csv("similar_channels.csv")
    # similar_channels_list = similar_channels_df['channels'].to_list()

    today = date.today()

    all_videos_df['most_views'] = all_videos_df['video_view_count'].astype(int).quantile(quantile)
    all_videos_df['well_performers'] = all_videos_df['video_view_count'].astype(float)>all_videos_df['most_views']
    all_videos_df['video_pub_date'] = pd.to_datetime(all_videos_df['video_pub_date']).dt.date

    outstanding_videos = all_videos_df[all_videos_df["well_performers"]]
    all_videos_df.to_csv("all_videos.csv")
    outstanding_videos.to_csv("outstanding_videos.csv")

    cutoff_date = today - pd.Timedelta(days=threshold)

    outstanding_videos['video_pub_date'] = pd.to_datetime(outstanding_videos['video_pub_date']).dt.date
    # outstanding_videos = outstanding_videos[outstanding_videos["video_pub_date"]>cutoff_date]

    # all_outstanding_videos = pd.DataFrame()

    # for channel_id in similar_channels_list:
    #     if os.path.exists(f'results/{channel_id}'):
    #         videos = pd.read_csv(f'results/{channel_id}/videos.csv')
    #         outstanding_videos = videos[videos["well_performers"]]
            
    #         # only get the videos made in the last 14 days
    #         cutoff_date = today - pd.Timedelta(days=threshold)

    #         outstanding_videos['video_pub_date'] = pd.to_datetime(outstanding_videos['video_pub_date']).dt.date
    #         outstanding_videos = outstanding_videos[outstanding_videos["video_pub_date"]>cutoff_date]
    #         all_outstanding_videos = all_outstanding_videos.append(outstanding_videos)

    print(outstanding_videos)
    outstanding_videos.to_csv("out.csv")
    # outstanding_videos.to_csv("analytics/all_outstanding_videos.csv")
    return outstanding_videos

    
