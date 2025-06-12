import pandas as pd
from textblob import TextBlob
import re

def clean_comment(text):
    text = re.sub(r"http\S+", "", text)  # remove URLs
    text = re.sub(r"@\w+", "", text)     # remove @mentions
    text = re.sub(r"#\w+", "", text)     # remove hashtags
    text = re.sub(r"[^A-Za-z0-9\s]+", "", text)  # remove special characters
    text = text.lower().strip()
    return text

def get_sentiment(polarity):
    if polarity > 0.1:
        return 'Positive'
    elif polarity < -0.1:
        return 'Negative'
    else:
        return 'Neutral'

# Load the comments
df = pd.read_csv('comments.csv')

# Clean and analyze
df['Cleaned'] = df['Comment'].apply(clean_comment)
df['Polarity'] = df['Cleaned'].apply(lambda x: TextBlob(x).sentiment.polarity)
df['Sentiment'] = df['Polarity'].apply(get_sentiment)

# Save results
df.to_csv('comments_with_sentiment.csv', index=False)
print("✅ Sentiment analysis complete. Results saved to 'comments_with_sentiment.csv'")
