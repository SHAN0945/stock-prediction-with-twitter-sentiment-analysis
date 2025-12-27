import sys
import asyncio
from twikit import Client, TooManyRequests
from transformers import pipeline
from datetime import datetime
from configparser import ConfigParser
from random import randint

async def analyze_sentiment(text: str):
    """Analyze sentiment asynchronously using Hugging Face model."""
    model = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    sentiment_task = pipeline("sentiment-analysis", model=model)
    return sentiment_task(text)

async def fetch_tweets(query: str, min_tweets: int = 100) -> list[dict]:
    """Fetch tweets asynchronously using Twikit."""
    
    # Read credentials from config
    config = ConfigParser()
    config.read('config.ini')
    username = config['X']['username']
    email = config['X']['email']
    password = config['X']['password']

    # Initialize client and authenticate
    client = Client(language='en-US')
    
    try:
        client.load_cookies('cookies.json')
    except FileNotFoundError:
        await client.login(auth_info_1=username, auth_info_2=email, password=password)
        client.save_cookies('cookies.json')

    tweet_count = 0
    all_tweets = []
    tweets = None

    while tweet_count < min_tweets:
        try:
            if tweets is None:
                print(f'{datetime.now()} - Initial search for "{query}"')
                tweets = await client.search_tweet(query, product='Top')
            else:
                wait_time = randint(5, 10)
                print(f'{datetime.now()} - Fetching next page in {wait_time}s...')
                await asyncio.sleep(wait_time)
                tweets = await tweets.next()

            for tweet in tweets:
                all_tweets.append({
                    'username': tweet.user.name,
                    'text': tweet.text,
                    'created_at': tweet.created_at,
                    'retweets': tweet.retweet_count,
                    'likes': tweet.favorite_count
                })
                tweet_count += 1

                if tweet_count >= min_tweets:
                    break

            print(f'{datetime.now()} - Collected {tweet_count} tweets')

        except TooManyRequests as e:
            reset_time = datetime.fromtimestamp(e.rate_limit_reset)
            wait_seconds = (reset_time - datetime.now()).total_seconds()
            print(f'Rate limited. Resuming at {reset_time}')
            await asyncio.sleep(wait_seconds)
            continue
        except Exception as e:
            print(f'Error: {str(e)}')
            break

    print(f'Completed. Collected {len(all_tweets)} tweets')
    return all_tweets[:min_tweets]  # Ensure exact count

async def main(input_data):
    """Fetch tweets, analyze sentiment, and count sentiment distribution asynchronously."""
    
    sentiment_result = {"positive": 0, "negative": 0, "neutral": 0}
    tweets = await fetch_tweets(input_data, 10)

    for tweet in tweets:
        print(tweet['text'])
        result = await analyze_sentiment(tweet['text'])

        sentiment_label = result[0]['label']
        if sentiment_label == 'positive':
            sentiment_result['positive'] += 1
        elif sentiment_label == 'negative':
            sentiment_result['negative'] += 1
        else:
            sentiment_result['neutral'] += 1
        
        print(result)

    print(sentiment_result)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sentiment_analysis.py '<search_query>'")
        sys.exit(1)

    search_query = sys.argv[1]
    asyncio.run(main(search_query))
