import streamlit as st
import pandas as pd
from outstanding_videos import get_outstanding_videos
from video_stats import get_video_stats

st.subheader("Step 1: Specify your YouTube API Key", divider="rainbow")
# youtube_api_key = "AIzaSyC_43cRsjiXhiepBELNQuwvfA6QaEanqyI"
youtube_api_key = st.text_input("Please enter your YouTube API Key")

# upload a list of similar channels
st.subheader("Step 2: Upload a CSV of similar channels", divider="rainbow")
st.write("If you don't upload anything a default file will be used.")
similar_channels = st.file_uploader("Choose a file")
if similar_channels is not None:
    similar_channels_df = pd.DataFrame(similar_channels, columns=["channels"])
    print(similar_channels_df)
    similar_channels_list = similar_channels_df['channels'].to_list()
else:
    similar_channels_df = pd.read_csv("similar_channels.csv")
    similar_channels_list = similar_channels_df['channels'].to_list()


st.subheader("Step 3: Set analysis options", divider="rainbow")
# How far back do you want to look?
st.write("Specify the time window you want to have here for the outstanding videos.")
threshold = st.slider('How far back do you want to look (days)?', 0, 60, 20)

# How many results do you want to get from each channel?
st.write("It is not possible to specify a date cutoff through YouTube's API when scraping videos from each channel. Instead you need to specify how many items to scrape. Higher the number, more likely that older videos will be scraped. But of course, more API credits need to be used.")
number_results = st.selectbox('How many videos from each channel do you want to include?', (10, 20, 30))

# What is an outstanding video for you?
st.write("Specify which quantile the video needs to be in a channel to be considered outstanding. Default=0.9")
quantile = st.slider('What is an outstanding video for you (quantile)?', 0.7, 0.99, 0.9)

start_analysis = st.button("Start analysis", type="primary")

@st.cache_resource
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

if start_analysis:
    get_video_stats(youtube_api_key, similar_channels_list, number_results, quantile)
    outstanding_videos = get_outstanding_videos(threshold)
    st.dataframe(outstanding_videos)

    csv = convert_df(outstanding_videos)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='outstanding_videos.csv',
        mime='text/csv',
    )


