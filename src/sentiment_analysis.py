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

def sentiment_results_and_counter(processed_data):
    """
    Count the number of positive, negative, and neutral sentiments in the processed data
    and store the results in a dictionary.

    @param processed_data: A list of [index, preprocessed_text] pairs.
    @ret: A dictionary with counts of each sentiment type and the processed results.
    """
    sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
    results = {"index": []}
    
    for item in processed_data:
        sentiment = sentiment_analyzer(item[1])
        results["index"].append([item[0], item[1], sentiment])
        
        # Update sentiment counters
        if sentiment == "Positive":
            sentiment_counts["positive"] += 1
        elif sentiment == "Negative":
            sentiment_counts["negative"] += 1
        else:
            sentiment_counts["neutral"] += 1
            
    return sentiment_counts, results