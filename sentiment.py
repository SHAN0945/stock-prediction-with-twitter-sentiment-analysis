from transformers import pipeline

def analyze_sentiment(query: str):
    model = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    sentiment_task = pipeline("sentiment-analysis", model=model)
    result = sentiment_task(query)
    return result