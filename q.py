import pandas as pd
from tweets import fetch_tweets 
from sentiment import analyze_sentiment
import asyncio


async def main(input_data):
    """Fetch tweets, analyze sentiment, and count sentiment distribution asynchronously."""
    
    sentiment_result = []
    tweets = await fetch_tweets(input_data, 10)

    for tweet in tweets:
        result = analyze_sentiment(tweet['text'])
        sentiment_label = result[0]['label']
        
        # Convert sentiment label to numerical score
        sentiment_score = 1 if sentiment_label == 'positive' else -1 if sentiment_label == 'negative' else 0

        # Append to list
        sentiment_result.append({
            'date': tweet['created_at'].date(),
            'sentiment_score': sentiment_score
        })
    
    # Convert to DataFrame
    sentiment_df = pd.DataFrame(sentiment_result)
    
    # Aggregate sentiment score per day
    sentiment_df = sentiment_df.groupby('date').mean().reset_index()

    # Save to CSV for integration
    sentiment_df.to_csv('sentiment_data.csv', index=False)
    print(sentiment_df.head())

asyncio.run(main("tesla"))