import torch
from transformers import AutoTokenizer


# https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment?library=transformers


#Load the Model from hugging face and the Tokenizer thats associated with Model
#text_series is a pandas series of text data

def tokenize_data(text_series):
    MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    
    #func to use the tokenizer loaded above for the max length allowed
    def tokenize(text):
        return tokenizer.encode(text, truncation=True, padding='max_length', max_length=512)
    
    #Applies the tokenize function to each element in the text_series Pandas Series.
    tokenized_texts = text_series.apply(tokenize)

    #input into torch - this Input_ids will be used for input into robberta model 
    input_ids = torch.tensor(tokenized_texts.tolist())

    # Create attention masks

    #Note from hugging face : 
    '''in transformer models like RoBERTa, attention masks are used to differentiate between actual 
    tokens and padding tokens in the input sequences. This is important because padding tokens 
    should not contribute to the model's understanding of the text.'''

    #The result is a list of lists (one list for each sequence in input_ids), 
    #where each inner list contains 1.0 for non-padding tokens and 0.0 for padding tokens.
    attention_masks = [[float(i != 0) for i in seq] for seq in input_ids]

    #converts the attention masks from a list of lists to a PyTorch tensor
    attention_masks = torch.tensor(attention_masks)
    
    return input_ids, attention_masks


