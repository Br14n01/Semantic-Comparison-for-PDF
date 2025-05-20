from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments
from data_loader import build_dataset
from dataset import SentimentDataset

# Paths to dataset files
dictionary_path = "./datasets/dictionary.txt"
sentiment_path = "./datasets/sentiment_labels.txt"
sentences_path = "./datasets/datasetSentences.txt"
splits_path = "./datasets/datasetSplit.txt"

# Load and build datasets
train_data, dev_data, test_data = build_dataset(dictionary_path, sentiment_path, sentences_path, splits_path)

# Initialize tokenizer and datasets
model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)

train_dataset = SentimentDataset(train_data, tokenizer)
dev_dataset = SentimentDataset(dev_data, tokenizer)

# Load model for regression (num_labels=1)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=1)

# Training arguments
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    save_strategy="epoch",
    learning_rate=2e-5,
    weight_decay=0.01,
    logging_dir="./logs",
    report_to="none"
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=dev_dataset
)

# Train the model
trainer.train()

# Save the fine-tuned model and tokenizer
model.save_pretrained("./results")
tokenizer.save_pretrained("./results")
