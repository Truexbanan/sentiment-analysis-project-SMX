import polars as pl
import torch
from transformers import AutoModelForSequenceClassification
from src.roberta_token import tokenize_data

# Define constants for the thresholds
NEUTRAL_THRESHOLD = 0.7
SLIGHT_THRESHOLD = 0.35

class DataFrameCreationError(Exception):
    pass

def create_dataframe(processed_data):
    """
    Create a Polars DataFrame from processed data.
    
    @param processed_data: List of processed data.
    @ret: Polars DataFrame.
    """
    try:
        return pl.DataFrame(processed_data, schema=["id", "text"])
    except Exception as e:
        print(f"Error creating DataFrame: {e}")
        raise DataFrameCreationError(f"Failed to create DataFrame: {e}")

def adjust_thresholds(logits, neutral_threshold=0.65, slight_threshold=0.4):
    """
    Adjust the thresholds for classification.

    @param logits: Model logits.
    @param neutral_threshold: Threshold for neutral classification.
    @param slight_threshold: Threshold for slight classification.
    @ret: List of adjusted predictions.
    """
    probabilities = torch.nn.functional.softmax(logits, dim=1)
    adjusted_predictions = []

    for prob in probabilities:
        highest_prob_class = torch.argmax(prob).item()
        highest_prob = prob[highest_prob_class]

        if highest_prob_class == 1 and highest_prob > neutral_threshold:
            adjusted_predictions.append(1)  # Neutral
        elif highest_prob_class == 2 and prob[1] > slight_threshold:
            adjusted_predictions.append(4)  # Slightly Positive
        elif highest_prob_class == 0 and prob[1] > slight_threshold:
            adjusted_predictions.append(3)  # Slightly Negative
        elif highest_prob_class == 2 and prob[1] <= slight_threshold:
            adjusted_predictions.append(2)  # Positive
        elif highest_prob_class == 0 and prob[1] <= slight_threshold:
            adjusted_predictions.append(0)  # Negative
        elif highest_prob_class == 1 and highest_prob <= neutral_threshold:
            second_highest_prob_class = torch.argsort(prob, descending=True)[1].item()
            if second_highest_prob_class == 0:
                adjusted_predictions.append(3)  # Slightly Negative
            elif second_highest_prob_class == 2:
                adjusted_predictions.append(4)  # Slightly Positive

    return adjusted_predictions

def roberta_analyze_data(raw_data):
    """
    Analyze data using the RoBERTa model.
    
    @param raw_data: Raw input data.
    @ret: List of analysis results.
    """
    try:
        df = create_dataframe(raw_data)
    except DataFrameCreationError as e:
        print(e)
        return

    input_ids, attention_masks = tokenize_data(df['text'].to_list())

    MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)

    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_masks)

    adjusted_predictions = adjust_thresholds(outputs.logits, neutral_threshold=NEUTRAL_THRESHOLD, slight_threshold=SLIGHT_THRESHOLD)

    labels = ["Negative", "Neutral", "Positive", "Slightly Negative", "Slightly Positive"]
    results = [[item[0], item[1], labels[pred]] for item, pred in zip(raw_data, adjusted_predictions)]

    return results
