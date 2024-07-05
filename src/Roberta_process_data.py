import pandas as pd
import torch
from transformers import AutoModelForSequenceClassification
from RobertaToken import tokenize_data

# Define a constant for the neutral threshold
NEUTRAL_THRESHOLD = 0.4


# for creating Pandas DF with error exception
class DataFrameCreationError(Exception):
    pass

def create_dataframe(processed_data):
    try:
        df = pd.DataFrame(processed_data, columns=['id', 'text'])
        return df
    except Exception as e:
        print(f"Error creating DataFrame: {e}")
        raise DataFrameCreationError(f"Failed to create DataFrame: {e}")



# This entire block is for Adjusting the thresholds for determining sentiment in order to reduce amount of neutral results
    
# logits - This parameter expects the raw output from the model
# neutral_threshold=0.6: This parameter sets a default threshold for determining whether a sentiment should be classified as neutral. 
# If the highest probability is below this threshold, the prediction is considered neutral.
    

# the lower the neutral_threshold means less neutral results and higher means more neutral.
    
# essentialy the threshold is saying that when the model's confidence (probability) for all classes is low it just assigns neutral
def adjust_thresholds(logits, neutral_threshold=0.6):

    # softmax function is a mathematical function that converts a vector of raw scores (logits) into probabilities - https://en.wikipedia.org/wiki/Softmax_function
    # Convert logits to probabilities that sum to 1
    # dim=1: Specifies to apply softmax along the columns (second dimension) of the tensor, which contain class scores for each example
    # dim = 0 would apply softmax across rows which would not make sense as rows = batch size

    # the tensor logits should be in the form of - (batch_size (rows) x num_classes (cols))

    probabilities = torch.nn.functional.softmax(logits, dim=1)

    
    adjusted_predictions = []

    # Iterates over each probability vector in the probabilities tensor. 
    #Each pr is a vector containing the probabilities for each class (negative, neutral, positive).
    for prob in probabilities:
        max_prob = torch.max(prob) # Find the highest probability in the current set of class probabilities
        if max_prob < neutral_threshold: # If the highest probability is less than the neutral threshold
            adjusted_predictions.append(1)  # Classify as neutral (1)
        else:
            adjusted_predictions.append(torch.argmax(prob).item()) # Otherwise, classify as the index of the highest probability (negative or positive)
    return adjusted_predictions



# to be called in main.py - returns a  a list of dictionaries containing the index, processed text, and sentiment 

def analyze_data(processed_data):
    # Convert to DataFrame for easier processing
    try:
        df = create_dataframe(processed_data)
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
    adjusted_predictions = adjust_thresholds(outputs.logits, neutral_threshold = NEUTRAL_THRESHOLD )

    # Map predictions to sentiment labels
    labels = ["Negative", "Neutral", "Positive"]
    results = [{"index": item[0], "text": item[1], "sentiment": labels[pred]} for item, pred in zip(processed_data, adjusted_predictions)]

    return results


