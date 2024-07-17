import pandas as pd
import torch
from transformers import AutoModelForSequenceClassification
from src.roberta_token import tokenize_data


# Define constants for the thresholds
# Amount of neutrals and NEUTRAL_THRESHOLD have an inverse relationship 

NEUTRAL_THRESHOLD = 0.65
SLIGHT_THRESHOLD = 0.4

class DataFrameCreationError(Exception):
    pass

#creating a pandas DF
def create_dataframe(processed_data):
    try:
        df = pd.DataFrame(processed_data, columns=['id', 'text'])
        return df
    except Exception as e:
        print(f"Error creating DataFrame: {e}")
        raise DataFrameCreationError(f"Failed to create DataFrame: {e}")


# logits - This parameter expects the raw output from the model
    
def adjust_thresholds(logits, neutral_threshold=0.65, slight_threshold=0.4):

    # softmax function is a mathematical function that converts a vector of raw scores (logits) into probabilities - https://en.wikipedia.org/wiki/Softmax_function
    # Convert logits to probabilities that sum to 1
    # dim=1: Specifies to apply softmax along the columns (second dimension) of the tensor, which contain class scores
    # the tensor logits should be in the form of - (batch_size (rows) x num_classes (cols))

    probabilities = torch.nn.functional.softmax(logits, dim=1)
    adjusted_predictions = []

    print(f"Adjusting threshold with {neutral_threshold} threshold value")

    # Iterates over each probability vector in the probabilities tensor. 
    # Each pr is a vector containing the probabilities for each class (negative, SN, neutral, SP, positive).

    for prob in probabilities:
        print(f"Probabilities: {prob.tolist()}")
        if prob[1] > neutral_threshold:  # Check if the neutral class exceeds the threshold
            print("Classified as Neutral")
            adjusted_predictions.append(1)  # Classify as neutral
        elif prob[0] > slight_threshold and prob[1] > slight_threshold:
            print("Classified as Slightly Negative")
            adjusted_predictions.append(3)  # Classify as slightly negative
        elif prob[2] > slight_threshold and prob[1] > slight_threshold:
            print("Classified as Slightly Positive")
            adjusted_predictions.append(4)  # Classify as slightly positive
        elif prob[0] > prob[2]:
            print("Classified as Negative")
            adjusted_predictions.append(0)  # Classify as negative
        else:
            print("Classified as Positive")
            adjusted_predictions.append(2)  # Classify as positive

    return adjusted_predictions


def roberta_analyze_data(raw_data):
    # Convert to DataFrame for easier processing
    try:
        df = create_dataframe(raw_data)
    except DataFrameCreationError as e:
        print(e)
        return

    # Tokenize and create attention masks
    input_ids, attention_masks = tokenize_data(df['text'])


    # Load the model

    MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)


    # removed gradiant calculation - to reduce memory consumption as its not needed unless we are using Tensor.backward()

    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_masks)



    # Extract the predicted sentiments
    # Adjust the thresholds to classify sentiments

    adjusted_predictions = adjust_thresholds(outputs.logits, neutral_threshold=NEUTRAL_THRESHOLD, slight_threshold=SLIGHT_THRESHOLD)

    labels = ["Negative", "Neutral", "Positive", "Slightly Negative", "Slightly Positive"]
    results = [[item[0], item[1], labels[pred]] for item, pred in zip(raw_data, adjusted_predictions)]


    return results
