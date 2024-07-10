import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd
from src.roberta_token import tokenize_data


data = {
    "index": [
        [1, "Rishi is awful."],
        [2, "I hate this guy."],
        [3, "I love Rishi."],
        [4, "I hate that I love Rishi."]
    ]
}


df = pd.DataFrame(data["index"], columns=['id', 'text'])


input_ids, attention_masks = tokenize_data(df['text'])


print("Input IDs:")
print(input_ids)
print("Attention Masks:")
print(attention_masks)


MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
model = AutoModelForSequenceClassification.from_pretrained(MODEL)


with torch.no_grad():
    outputs = model(input_ids, attention_mask=attention_masks)


predictions = torch.argmax(outputs.logits, dim=1)


labels = ["Negative", "Neutral", "Positive"]
results = [labels[pred] for pred in predictions]


for text, result in zip(df['text'], results):
    print(f"Text: {text}\nSentiment: {result}\n")
