import matplotlib.pyplot as plt
import pandas as pd
from tabulate import tabulate

def print_sentiment_analysis(sentiment_counts):
    """
    Print the sentiment counts in a formatted table.

    @param sentiment_counts: A dictionary with counts of each sentiment type.
    @ret: None.
    """
    original_counts = {
        "positive": 1503,
        "negative": 429,
        "neutral": 623
    }

    table_data = [
        ["Positive", original_counts["positive"], sentiment_counts.get("Positive", 0)],
        ["Negative", original_counts["negative"], sentiment_counts.get("Negative", 0)],
        ["Neutral", original_counts["neutral"], sentiment_counts.get("Neutral", 0)]
    ]

    headers = ["Sentiment", "Original", "VADER"]

    print(tabulate(table_data, headers=headers, tablefmt="grid"))

def visualize_sentiment(data):
    """
    Visualize the sentiment analysis results in a pie chart.

    @param data: A list of [index, text, sentiment] pairs.
    @ret: None.
    """
    df = pd.DataFrame(data, columns=['Index', 'Text', 'Sentiment'])

    # Count the number of each sentiment
    sentiment_counts = df['Sentiment'].value_counts()

    # Plotting the sentiment distribution as a pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=140, colors=['#66b3ff','#99ff99','#ffcc99'])
    plt.title('Distribution of Sentiment Scores')
    plt.show()