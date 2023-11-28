import pandas as pd
from datetime import date
import requests
import json

api_key = "AIzaSyC_43cRsjiXhiepBELNQuwvfA6QaEanqyI"

today = date.today()

similar_channels_df = pd.read_csv("similar_channels.csv")
similar_channels_list = similar_channels_df['channels'].to_list()

collected_info = []

for channel_id in similar_channels_list:
    channel_data = {}

    channel_info_url = f'https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2Cstatistics&id={channel_id}&key={api_key}'
    json_channel_info = requests.get(channel_info_url)
    channel_data = json.loads(json_channel_info.text)

    channel_name = channel_data['items'][0]['snippet']['title']
    subscriber_count = channel_data['items'][0]['statistics']['subscriberCount']
    video_count = channel_data['items'][0]['statistics']['videoCount']
    channel_view_count = channel_data['items'][0]['statistics']['viewCount']

    channel_data = {"channel_id":channel_id,"date":today,"channel_name":channel_name,"subscriber_count":subscriber_count,"video_count":video_count,"channel_view_count":channel_view_count}
    collected_info.append(channel_data)

collected_info_df = pd.DataFrame(collected_info)
collected_info_df.to_csv("channels_latest_data.csv")
print(collected_info_df)



