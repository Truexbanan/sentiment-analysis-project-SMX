from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def sentiment_analyzer(text):
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