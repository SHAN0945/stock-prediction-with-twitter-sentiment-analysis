import tweets
import sentiment
import asyncio
import sys

if(__name__ == '__main__'):
    sentimentResult = {"positive": 0, "negative": 0, "neutral": 0}
    
    async def main(input_data):
        tweets1 = await tweets.fetch_tweets(input_data, 10)
        
        for tweet in tweets1:
            print(tweet['text'])
            result = sentiment.analyze_sentiment(tweet['text'])
            if result[0]['label'] == 'positive':
                sentimentResult['positive'] += 1
            elif result[0]['label'] == 'negative':
                sentimentResult['negative'] += 1
            else:
                sentimentResult['neutral'] += 1
            print(result)
        print(sentimentResult)
        
    input_data = sys.argv[1]
    print(input_data)
    asyncio.run(main(input_data))