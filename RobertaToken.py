import torch
from transformers import AutoTokenizer


#Load the Model from hugging face and the Tokenizer thats associated with Model
def tokenize_data(text_series):
    MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    
    #func to use the tokenizer loaded above for the max length allowed
    def tokenize(text):
        return tokenizer.encode(text, truncation=True, padding='max_length', max_length=512)
    
    tokenized_texts = text_series.apply(tokenize)
    input_ids = torch.tensor(tokenized_texts.tolist())
