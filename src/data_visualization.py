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