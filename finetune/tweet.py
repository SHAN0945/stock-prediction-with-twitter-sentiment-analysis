from twikit import Client, TooManyRequests
from datetime import datetime, timedelta
from configparser import ConfigParser
import asyncio
import re
import csv
import os
from random import randint

def clean_text(text: str) -> str:
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[\U00010000-\U0010FFFF]', '', text)
    text = re.sub(r'\\[nrt]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

async def fetch_tweets(query: str, min_tweets: int = 30) -> list[dict]:
    config = ConfigParser()
    config.read('config.ini')
    username = config['X']['username']
    email = config['X']['email']
    password = config['X']['password']

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
                print(f'{datetime.now()} - Searching for "{query}"')
                tweets = await client.search_tweet(query, product='Top')
            else:
                wait_time = randint(5, 10)
                print(f'{datetime.now()} - Fetching next page in {wait_time}s...')
                await asyncio.sleep(wait_time)
                tweets = await tweets.next()

            for tweet in tweets:
                cleaned_text = clean_text(tweet.text)
                all_tweets.append({
                    'created_at': tweet.created_at,
                    'text': cleaned_text,
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

    return all_tweets[:min_tweets]

def save_to_csv(tweets: list[dict], filename: str = 'tweets15tsla.csv'):
    fieldnames = ['Date', 'Tweet', 'Stock Name', 'Company Name']
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerows(tweets)

async def main():
    # Define date range
    start_date = datetime.strptime("2025-02 -01", "%Y-%m-%d")
    end_date = datetime.strptime("2025-04-15", "%Y-%m-%d")
    
    # Generate all dates in range
    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        current_date += timedelta(days=1)

    # Define stock queries
    stock_queries = [
        # ('(from:$amzn)', 'AMZN', 'Amazon'),
        # ('(from:$aapl)', 'AAPL', 'Apple Inc.'),
        ('(from:$tsla)', 'TSLA', 'Tesla'),
        # Add more stocks as needed
    ]

    for date in dates:
        since_date = date.strftime("%Y-%m-%d")
        until_date = (date + timedelta(days=1)).strftime("%Y-%m-%d")
        
        for base_query, stock_symbol, company_name in stock_queries:
            query = f"{base_query} lang:en since:{since_date} until:{until_date}"
            print(f"\nFetching tweets for {stock_symbol} on {since_date}")
            
            raw_tweets = await fetch_tweets(query)
            
            processed_tweets = []
            for tweet in raw_tweets:
                processed_tweets.append({
                    'Date': tweet['created_at'],
                    'Tweet': tweet['text'],
                    'Stock Name': stock_symbol,
                    'Company Name': company_name
                })
            
            save_to_csv(processed_tweets)
    
    print("\nAll data collected and saved to tweets.csv")

if __name__ == "__main__":
    asyncio.run(main())