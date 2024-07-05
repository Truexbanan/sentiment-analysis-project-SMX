from transformers import Trainer, TrainingArguments, AutoTokenizer, AutoModelForSequenceClassification
from datasets import Dataset
import torch

def fine_tune_model(processed_data):
    # Load pre-trained model and tokenizer
    MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL, num_labels=3)

    # Freeze all layers except the last ones
    for param in model.roberta.parameters():
        param.requires_grad = False
    for param in model.classifier.parameters():
        param.requires_grad = True

    # Create a custom dataset
    data = {
        'text': [item[1] for item in processed_data],
        'labels': [item[2] for item in processed_data]  # Assuming the sentiment labels are available
    }
    dataset = Dataset.from_dict(data)

    # Tokenize the dataset
    def preprocess_function(examples):
        return tokenizer(examples['text'], truncation=True, padding=True)

    encoded_dataset = dataset.map(preprocess_function, batched=True)

    # Define training arguments
    training_args = TrainingArguments(
        output_dir='./results',
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=3,
        weight_decay=0.01,
    )

    # Define Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=encoded_dataset,
        eval_dataset=encoded_dataset,
    )

    # Fine-tune the model
    trainer.train()
