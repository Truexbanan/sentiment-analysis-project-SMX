import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def VADER_sentiment_analyzer(text):
    """
    Analyze the sentiment of the text using VADER.

    @param text: The text to analyze.
    @ret: The corresponding sentiment ('Positive', 'Negative', 'Neutral')
    """
    # Initialize the VADER sentiment analyzer
    analyzer = SentimentIntensityAnalyzer()

    sentiment = analyzer.polarity_scores(text)
    if sentiment['compound'] >= 0.05:
        return "Positive"
    elif sentiment['compound'] <= -0.05:
        return "Negative"
    else:
        return "Neutral"

def count_sentiments(data):
    """
    Count the number of each sentiment type in the data.

    @param data: A list of [index, text, sentiment] pairs.
    @ret: A dictionary with counts of each sentiment type.
    """
    df = pd.DataFrame(data, columns=['Index', 'Text', 'Sentiment'])
    
    # Count the number of each sentiment
    sentiment_counts = df['Sentiment'].value_counts().to_dict()
    return sentiment_counts