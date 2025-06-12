import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Load data
df = pd.read_csv('comments_with_sentiment.csv')

# Pie Chart of Sentiment
sentiment_counts = df['Sentiment'].value_counts()

plt.figure(figsize=(6, 6))
plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', colors=['green', 'grey', 'red'])
plt.title('Sentiment Distribution')
plt.savefig('sentiment_pie_chart.png')
plt.show()

# WordCloud (only for positive + negative)
all_words = ' '.join(df[df['Sentiment'] != 'Neutral']['Cleaned'])

wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_words)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of YouTube Comments')
plt.savefig('wordcloud.png')
plt.show()
