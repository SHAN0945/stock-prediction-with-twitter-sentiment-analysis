    new_tweets = pd.read_csv('/content/tweets.csv')
    df = new_tweets[new_tweets['Stock Name'] == stock_name]
    sent_df = df.copy()
    sent_df["sentiment_score"] = ''
    sent_df["Negative"] = ''
    sent_df["Neutral"] = ''
    sent_df["Positive"] = ''

    import nltk
    nltk.download('vader_lexicon')

    sentiment_analyzer = SentimentIntensityAnalyzer()
    for indx, row in sent_df.T.items():
        try:
            sentence_i = unicodedata.normalize('NFKD', sent_df.loc[indx, 'Tweet'])
            sentence_sentiment = sentiment_analyzer.polarity_scores(sentence_i)
            sent_df.at[indx, 'sentiment_score'] = sentence_sentiment['compound']
            sent_df.at[indx, 'Negative'] = sentence_sentiment['neg']
            sent_df.at[indx, 'Neutral'] = sentence_sentiment['neu']
            sent_df.at[indx, 'Positive'] = sentence_sentiment['pos']
        except TypeError:
            print (sent_df.loc[indx, 'Tweet'])
            print (indx)
            break

    sent_df['Date'] = pd.to_datetime(sent_df['Date'])
    sent_df['Date'] = sent_df['Date'].dt.date
    sent_df = sent_df.drop(columns=['Negative', 'Positive', 'Neutral', 'Stock Name', 'Company Name'])

    twitter_df = sent_df.groupby('Date')['sentiment_score'].mean()
    twitter_df = twitter_df.to_frame(name='sentiment_score')

    stock_df = all_stocks[all_stocks['Stock Name'] == stock_name.lower()]
    stock_df['Date'] = pd.to_datetime(stock_df['Date'])
    stock_df['Date'] = stock_df['Date'].dt.date
    final_df = stock_df.join(twitter_df, how="left", on="Date")
    final_df = final_df.drop(columns=['Stock Name'])
    final_df['Close'] = pd.to_numeric(final_df['Close'], errors='coerce')
    tech_df = get_tech_ind(final_df)
    dataset = tech_df.iloc[20:,:].reset_index(drop=True)
    dataset.iloc[:, 1:] = pd.concat([dataset.iloc[:, 1:].ffill()])
    datetime_series = pd.to_datetime(dataset['Date'])
    datetime_index = pd.DatetimeIndex(datetime_series.values)
    dataset = dataset.set_index(datetime_index)
    dataset = dataset.sort_values(by='Date')
    dataset = dataset.drop(columns='Date')
    X_scale_dataset,y_scale_dataset = normalize_data(dataset, (-1,1), "Close")
    X_batched, y_batched, yc = batch_data(X_scale_dataset, y_scale_dataset, batch_size = 5, predict_period = 1)
    predicted_test_data = eval_op(test_generator, X_batched)
    print(predicted_test_data)
