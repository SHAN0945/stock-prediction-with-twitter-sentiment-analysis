# stock_prediction_gan.py
import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from pickle import load
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.preprocessing import MinMaxScaler

# ----------------------------
# 1. Sentiment Analysis Module
# ----------------------------
def process_tweets(tweet_file: str, stock_data: pd.DataFrame) -> pd.DataFrame:
    """
    Process raw tweet data and merge with stock data
    Returns DataFrame with dates and sentiment scores
    """
    # Load and preprocess tweets
    tweets = pd.read_csv(tweet_file)
    tweets['Date'] = pd.to_datetime(tweets['Date'].str.split('+').str[0], format='%a %b %d %H:%M:%S %Y')
    tweets['date'] = tweets['Date'].dt.normalize()
    
    # Calculate sentiment scores
    analyzer = SentimentIntensityAnalyzer()
    tweets['sentiment'] = tweets['Tweet'].progress_apply(lambda x: analyzer.polarity_scores(x)['compound'])
    
    # Merge with stock data
    daily_sentiment = tweets.groupby('date')['sentiment'].mean().reset_index()
    merged_data = pd.merge(stock_data, daily_sentiment, left_index=True, right_on='date', how='left')
    
    # Fill missing sentiment scores
    merged_data['sentiment'].fillna(0, inplace=True)
    return merged_data.set_index('date')

# ----------------------------
# 2. Data Preparation
# ----------------------------
def load_and_prepare_data(stock_file: str, tweet_file: str):
    """
    Load and merge stock data with sentiment scores
    Returns scaled sequences and original data
    """
    # Load raw data
    stock_data = pd.read_csv(stock_file, index_col='Date', parse_dates=True)
    
    # Process tweets and merge
    merged_data = process_tweets(tweet_file, stock_data)
    
    # Load scalers
    X_scaler = load(open('X_scaler.pkl', 'rb'))
    Y_scaler = load(open('Y_scaler.pkl', 'rb'))
    
    # Create sequences
    sequence_length = 30  # Update with your trained model's sequence length
    features = ['Open', 'High', 'Low', 'Close', 'Volume', 'sentiment']  # Match training features
    
    # Normalize and create sequences
    scaled_data = X_scaler.transform(merged_data[features])
    X, y = [], []
    for i in range(len(scaled_data) - sequence_length):
        X.append(scaled_data[i:i+sequence_length])
        y.append(scaled_data[i+sequence_length, 3])  # Close price as target
    
    return np.array(X), np.array(y), merged_data.index[sequence_length:]

# ----------------------------
# 3. Model Evaluation
# ----------------------------
def evaluate_gan(generator_path: str, X_test: np.ndarray, y_test: np.ndarray, index_test: pd.DatetimeIndex):
    """
    Generate predictions and plot results
    """
    # Load model and scalers
    generator = tf.keras.models.load_model(generator_path)
    Y_scaler = load(open('Y_scaler.pkl', 'rb'))
    
    # Generate predictions
    scaled_preds = generator.predict(X_test)
    predictions = Y_scaler.inverse_transform(scaled_preds[:, 3].reshape(-1, 1)).flatten()
    
    # Inverse transform actual values
    actual_prices = Y_scaler.inverse_transform(y_test.reshape(-1, 1)).flatten()
    
    # Plot results
    plt.figure(figsize=(14, 6))
    plt.plot(index_test, actual_prices, label='Actual Prices', alpha=0.7)
    plt.plot(index_test, predictions, '--', label='GAN Predictions', alpha=0.9)
    plt.title('Stock Price Prediction vs Actual', fontsize=14)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Price (USD)', fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.show()
    
    return predictions

# ----------------------------
# 4. Main Execution
# ----------------------------
if __name__ == "__main__":
    # Configuration
    STOCK_FILE = 'your_stock_data.csv'  # Replace with your file
    TWEET_FILE = 'your_tweet_data.csv'  # Replace with your file
    GENERATOR_PATH = 'generator_model.h5'  # Trained GAN generator
    
    # Load and prepare data
    X_test, y_test, test_dates = load_and_prepare_data(STOCK_FILE, TWEET_FILE)
    
    # Generate predictions and plot
    predictions = evaluate_gan(GENERATOR_PATH, X_test, y_test, test_dates)
    
    # Print next 7 days predictions
    print("\nNext 7 Trading Days Predictions:")
    for date, price in zip(test_dates[-7:], predictions[-7:]):
        print(f"{date.strftime('%Y-%m-%d')}: ${price:.2f}")
