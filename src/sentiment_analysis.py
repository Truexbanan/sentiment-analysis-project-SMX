from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def vader_sentiment_analyzer(text):
    """
    Analyze the sentiment of the text using VADER and apply custom rules.

    @param text: The text to analyze.
    @ret: A dictionary containing the sentiment scores.
    """
    # Initialize the VADER sentiment analyzer
    analyzer = SentimentIntensityAnalyzer()

    sentiment = analyzer.polarity_scores(text)

    # Custom rules for specific phrases:
    custom_rules = {
        "achievement": 0.2,
        "backlash": -0.3,
        "bankruptcy": -0.6,
        "bravery": 0.3,
        "challenge": 0,
        "courage": 0.3,
        "cut sanitation services": -0.5,
        "darkest hour": 0,
        "dim lights": -0.4,
        "energy": 0,
        "fear": -0.6,
        "flee": -0.7,
        "forced": -0.5,
        "heroism": 0.2,
        "inspiration": 0.2,
        "lead": 0,
        "livelihood": 0,
        "party": 0,  # Usually reference political party
        "play": 0,
        "struggle": -0.4,
        "support": 0.2,
        "thank": 0.3,
        "threaten": -0.7,
        "unity": 0.2,
        "united kingdom": 0,
        "united states": 0,
        "united nations": 0,
        "victory": 0.2
    }
    
    positive_words = ["love", "loved", "great", "excellent", "fantastic", "wonderful"]

    # Analyze the sentiment of the text using VADER
    sentiment = analyzer.polarity_scores(text)
    
    # Apply custom rules
    text_lower = text.lower()
    for phrase, adjustment in custom_rules.items():
        if phrase in text_lower:
            sentiment['compound'] -= analyzer.polarity_scores(phrase)['compound']
            sentiment['compound'] += adjustment
    
    # Detect overall negativity and adjust positive words
    if sentiment['compound'] < -0.5:
        for word in positive_words:
            if word in text_lower:
                sentiment['compound'] -= analyzer.polarity_scores(word)['compound']

    return sentiment

def vader_sentiment_label(sentiment):
    """
    Label the sentiment based on the sentiment scores.

    @param sentiment: The sentiment score to label.
    @ret: The corresponding sentiment ('Positive', 'Negative', 'Neutral')
    """
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
    sentiment_counts = {}

    for _, _, sentiment in data:
        if sentiment in sentiment_counts:
            sentiment_counts[sentiment] += 1
        else:
            sentiment_counts[sentiment] = 1

    return sentiment_counts