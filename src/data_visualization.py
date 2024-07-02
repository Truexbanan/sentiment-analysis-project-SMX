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
    wedges, _, percentage_texts = plt.pie(
        sentiment_counts,
        labels=[''] * len(sentiment_counts),
        autopct='%1.1f%%',
        startangle=140,
        colors=['#00CC44','#F6AE28','#ED4545'],
        textprops={'fontsize': 14, 'fontweight': 'bold'}
    )
    # Set the font size for the percentage values
    for percentage in percentage_texts:
        percentage.set_fontsize(16)

    plt.title('Distribution of Sentiment Scores', fontsize=20, fontweight='bold')
    plt.legend(wedges, sentiment_counts.index, title="Sentiment Categories", fontsize=12, title_fontsize='13')
    plt.show()