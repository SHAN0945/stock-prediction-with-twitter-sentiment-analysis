from twikit import Client, TooManyRequests
from datetime import datetime
from configparser import ConfigParser
from random import randint
import asyncio

async def fetch_tweets(query: str, min_tweets: int = 100) -> list[dict]:
   
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
        await client.login(
            auth_info_1=username,
            auth_info_2=email,
            password=password
        )
        client.save_cookies('cookies.json')

    tweet_count = 0
    all_tweets = []
    tweets = None

    while tweet_count < min_tweets:
        try:
            # Get initial batch or next page of tweets
            if tweets is None:
                print(f'{datetime.now()} - Initial search for "{query}"')
                tweets = await client.search_tweet(query, product='Top')
            else:
                wait_time = randint(5, 10)
                print(f'{datetime.now()} - Fetching next page in {wait_time}s...')
                await asyncio.sleep(wait_time)
                tweets = await tweets.next()

            # Process current batch of tweets
            for tweet in tweets:
                all_tweets.append({
                    'username': tweet.user.name,
                    'text': tweet.text,
                    'created_at': tweet.created_at,
                    'retweets': tweet.retweet_count,
                    'likes': tweet.favorite_count
                })
                tweet_count += 1

                # Exit if we've reached desired count
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

# Example usage
if __name__ == "__main__":
    sample_query = '(from:microsoft) lang:en until:2026-01-01 since:2018-01-01'
    
    async def main():
        tweets = await fetch_tweets(sample_query, 50)
        print(f"First tweet: {tweets[0]}")
    
    asyncio.run(main())