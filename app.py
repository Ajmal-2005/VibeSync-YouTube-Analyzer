import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re

# 🚀 App Config
st.set_page_config(page_title="VibeSync", page_icon="🎧", layout="centered")

# 💫 Welcome Header
st.markdown("""
    <h1 style='text-align: center; color: #00ADB5; font-size: 48px;'>🎧 VibeSync</h1>
    <h4 style='text-align: center; color: #6c6c6c;'>Sync with YouTube's emotions. Analyze any video's vibe instantly.</h4>
    <hr style='margin-top: 20px; margin-bottom: 20px;'/>
""", unsafe_allow_html=True)

# Setup YouTube API
API_KEY = 'AIzaSyB_NVbsr-C4f_m3fInWxIXGRnw_BXqb274'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def extract_video_id(url):
    if "v=" in url:
        return url.split("v=")[1][:11]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1][:11]
    return None

def get_comments(video_id, max_comments=100):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
    comments = []
    next_page_token = None

    while len(comments) < max_comments:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            textFormat="plainText",
            pageToken=next_page_token
        )
        response = request.execute()
        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return comments[:max_comments]

def clean_comment(text):
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"#\w+", "", text)
    text = re.sub(r"[^A-Za-z0-9\s]+", "", text)
    return text.lower().strip()

def analyze_sentiment(text):
    return TextBlob(text).sentiment.polarity

def classify_sentiment(polarity):
    if polarity > 0.1:
        return 'Positive'
    elif polarity < -0.1:
        return 'Negative'
    else:
        return 'Neutral'

# Streamlit UI
st.title("🎥 YouTube Comment Sentiment Analyzer")
video_url = st.text_input("Paste a YouTube video URL:")

if st.button("Analyze"):
    try:
        video_id = extract_video_id(video_url)
        with st.spinner("Fetching comments..."):
            comments = get_comments(video_id)
        df = pd.DataFrame(comments, columns=["Comment"])
        df["Cleaned"] = df["Comment"].apply(clean_comment)
        df["Polarity"] = df["Cleaned"].apply(analyze_sentiment)
        df["Sentiment"] = df["Polarity"].apply(classify_sentiment)

        # Show basic stats
        st.subheader("📊 Sentiment Distribution")
        st.write(df["Sentiment"].value_counts())

        # Pie Chart
        fig1, ax1 = plt.subplots()
        df["Sentiment"].value_counts().plot.pie(autopct='%1.1f%%', colors=['green', 'gray', 'red'], ax=ax1)
        st.pyplot(fig1)

        # WordCloud
        st.subheader("☁️ Word Cloud")
        all_words = ' '.join(df[df["Sentiment"] != "Neutral"]["Cleaned"])
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_words)
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        ax2.imshow(wordcloud, interpolation='bilinear')
        ax2.axis('off')
        st.pyplot(fig2)

        # Table
        st.subheader("📋 All Comments with Sentiment")
        st.dataframe(df)

        # Download CSV
        st.download_button("📥 Download Results as CSV", df.to_csv(index=False), file_name="yt_sentiment.csv")

        
        pos = df['Sentiment'].value_counts().get('Positive', 0)
        neg = df['Sentiment'].value_counts().get('Negative', 0)
        emoji = "😃" if pos > neg else "😐" if pos == neg else "😢"
        st.subheader(f"Overall Video Mood: {emoji}")

    except Exception as e:
        st.error(f"Something went wrong: {e}")
