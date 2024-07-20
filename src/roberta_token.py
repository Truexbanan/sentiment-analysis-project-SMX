import torch
from transformers import AutoTokenizer
import polars as pl

def tokenize_data(text_series):
    """
    Tokenize the text data using a pre-trained tokenizer from Hugging Face.
    
    @param text_series: A list of text data to be tokenized.
    @ret: Tensors of input_ids and attention_masks for the model.
    """
    MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    
    def tokenize(text):
        """
        Tokenize the given text.
        
        @param text: The text to tokenize.
        @ret: Tokenized text.
        """
        return tokenizer.encode(text, truncation=True, padding='max_length', max_length=512)
    
    tokenized_texts = [tokenize(text) for text in text_series]

    input_ids = torch.tensor(tokenized_texts)

    # Create attention masks
    attention_masks = [[float(i != 0) for i in seq] for seq in input_ids]
    attention_masks = torch.tensor(attention_masks)
    
    return input_ids, attention_masks
