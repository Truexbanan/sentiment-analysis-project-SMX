import pandas as pd
import torch
from transformers import AutoModelForSequenceClassification
from RobertaToken import tokenize_data

# Define a constant for the neutral threshold
# Amount of neutrals and NEUTRAL_THRESHOLD have an inverse relationship 
NEUTRAL_THRESHOLD = 0.99

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
    
def adjust_thresholds(logits, neutral_threshold=0.65):

    # softmax function is a mathematical function that converts a vector of raw scores (logits) into probabilities - https://en.wikipedia.org/wiki/Softmax_function
    # Convert logits to probabilities that sum to 1
    # dim=1: Specifies to apply softmax along the columns (second dimension) of the tensor, which contain class scores
    # the tensor logits should be in the form of - (batch_size (rows) x num_classes (cols))

    probabilities = torch.nn.functional.softmax(logits, dim=1)
    adjusted_predictions = []

    print(f"Adjusting threshold with {neutral_threshold} threshold value")


   # Iterates over each probability vector in the probabilities tensor. 
    #Each pr is a vector containing the probabilities for each class (negative, neutral, positive).

    for prob in probabilities:
        print(f"Probabilities: {prob.tolist()}")
        if prob[1] > neutral_threshold:  # Check if the neutral class exceeds the threshold
            print("Classified as Neutral")
            adjusted_predictions.append(1)  # Classify as neutral
        else:
            highest_prob_class = torch.argmax(prob).item()
            if highest_prob_class == 1:  # If the highest probability is neutral, but it doesn't exceed the threshold, pick the next highest class
                non_neutral_probs = [prob[0], prob[2]]
                highest_non_neutral_class = torch.argmax(torch.tensor(non_neutral_probs)).item()
                adjusted_predictions.append(highest_non_neutral_class if highest_non_neutral_class == 0 else 2)
                print(f"Classified as {highest_non_neutral_class if highest_non_neutral_class == 0 else 2}")
            else:
                print(f"Classified as {highest_prob_class}")
                adjusted_predictions.append(highest_prob_class)  # Otherwise, classify as the highest probability class (negative or positive)

    return adjusted_predictions

def analyze_data(raw_data):
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

    adjusted_predictions = adjust_thresholds(outputs.logits, neutral_threshold=NEUTRAL_THRESHOLD)

    labels = ["Negative", "Neutral", "Positive"]
    results = [{"index": item[0], "text": item[1], "sentiment": labels[pred]} for item, pred in zip(raw_data, adjusted_predictions)]

    return results
