from googleapiclient.discovery import build
import pandas as pd

# Replace with your API key
API_KEY = 'AIzaSyB_NVbsr-C4f_m3fInWxIXGRnw_BXqb274'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

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

# Run the code
if __name__ == "__main__":
    video_url = input("Enter YouTube video URL: ")
    video_id = video_url.split("v=")[-1][:11]  # simple extract
    comments = get_comments(video_id)

    df = pd.DataFrame(comments, columns=["Comment"])
    df.to_csv("comments.csv", index=False)
    print(f"✅ {len(comments)} comments saved to comments.csv")
