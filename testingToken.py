import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd

# Import the tokenize_data function
from RobertaToken import tokenize_data

# Example text data
data = {
    "index": [
        [1, "Darkest Hour is a 2017 British biographical war drama film about Winston Churchill."],
        [2, "Millionaires are fleeing Britain in their thousands: Prime Minister Rishi Sunak and his wife."],
        [3, "Reap what you sow. The U.K. general election is still weeks away."],
        [4, "News and communications: The Rt Hon Rishi Sunak ... Joint statement by the spokespeople."],
        [5, "I hate rishi sunak and he is an awful person."],
        [6, "I love rishi sunak and he is a great person."],
        [7, "I hate how much I love rishi sunak."],
        
    ]
}

# Convert to DataFrame
df = pd.DataFrame(data["index"], columns=['id', 'text'])

# Tokenize and create attention masks
input_ids, attention_masks = tokenize_data(df['text'])

# Display the results
print("Input IDs:")
print(input_ids)
print("Attention Masks:")
print(attention_masks)

# Load the model
MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

# Perform model inference
with torch.no_grad():
    outputs = model(input_ids, attention_mask=attention_masks)

# Extract the predicted sentiments
predictions = torch.argmax(outputs.logits, dim=1)

# Map predictions to sentiment labels
labels = ["Negative", "Neutral", "Positive"]
results = [labels[pred] for pred in predictions]

# print the result
for text, result in zip(df['text'], results):
    print(f"Text: {text}\nSentiment: {result}\n")
