import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize the VADER sentiment analyzer once
vader_analyzer = SentimentIntensityAnalyzer()

def vader_analyze_sentiment(text):
    """
    Analyze the sentiment of the text using VADER and apply custom rules.

    @param text (str): The text to analyze.
    @ret (dict): A dictionary containing the sentiment scores:
        - 'neg' (float): Negative sentiment score.
        - 'neu' (float): Neutral sentiment score.
        - 'pos' (float): Positive sentiment score.
        - 'compound' (float): Compound sentiment score.
    """
    sentiment = vader_analyzer.polarity_scores(text)

    custom_rules = {
        "achievement": 0.2,
        "backlash": -0.3,
        "bankruptcy": -0.6,
        "bravery": 0.3,
        "challenge": -0.2,
        "courage": 0.3,
        "dim lights": -0.4,
        "fear": -0.6,
        "flee": -0.7,
        "forced": -0.5,
        "heroism": 0.2,
        "inspiration": 0.2,
        "struggle": -0.4,
        "support": 0.3,
        "thank": 0.3,
        "threaten": -0.7,
        "unity": 0.2,
        "victory": 0.2,
        "abysmal": -0.5,
        "ail": -0.4,
        "broken": -0.5,
        "poor": -0.3,
        "weird": -0.45,
        "cut sanitation services": -0.5,
        "not heartless cynical": -0.65,
        "invite": 0.15,
        "r e p e n t": -0.2,
        "like": 0,
        "committed": 0,
        "darkest hour": 0,
        "energy": 0,
        "lead": 0,
        "livelihood": 0,
        "party": 0,  # Usually reference political party
        "play": 0,
        "great britain": 0,
        "united kingdom": 0,
        "united states": 0,
        "united nations": 0
    }
    
    positive_words = ["love", "loved", "great", "excellent", "fantastic", "wonderful"]

    # Fine-tune the sentiment score based on specific rules
    for phrase, adjustment in custom_rules.items():
        if phrase in text.lower():
            sentiment['compound'] -= vader_analyzer.polarity_scores(phrase)['compound']
            sentiment['compound'] += adjustment
    
    # If overall sentiment should be negative, adjust presence of positive words
    if sentiment['compound'] < -0.2:
        for word in positive_words:
            if word in text.lower():
                sentiment['compound'] -= vader_analyzer.polarity_scores(word)['compound']

    return sentiment

def vader_label_sentiment(sentiment):
    """
    Label the sentiment based on the sentiment scores.

    @param sentiment (dict): The sentiment score to label, including 'compound' key.
    @ret (str): The corresponding sentiment label as a string ('Positive', 'Negative', 'Neutral').
    """
    if sentiment['compound'] >= 0.05:
        return "Positive"
    elif sentiment['compound'] <= -0.05:
        return "Negative"
    else:
        return "Neutral"

def vader_analyze_batch(data):
    """
    Analyze sentiments for a batch of data items.

    @param data (np.ndarray): A NumPy array of [index, text] pairs.
    @ret (np.ndarray): A NumPy array of [index, text, sentiment_label] pairs.
    """
    # Convert to NumPy array if not already
    if not isinstance(data, np.ndarray):
        data = np.array(data)

    results = []
    for index, text in data:
        sentiment = vader_analyze_sentiment(text)
        sentiment_label = vader_label_sentiment(sentiment)
        results.append([index, text, sentiment_label])

    return np.array(results)