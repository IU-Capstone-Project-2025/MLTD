import torch
import numpy as np
import pandas as pd
from torch.utils.data import Dataset
from transformers import BertTokenizer, BertForSequenceClassification, TrainingArguments, Trainer
from transformers import DataCollatorWithPadding


class TextDataset(Dataset):
    def __init__(self, texts, tokenizer, max_length=128):
        self.texts = texts
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        encoding = self.tokenizer(
            text,
            truncation=True,
            max_length=self.max_length,
            padding=False,
            return_tensors=None
        )
        return encoding


def analyze(filename):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = BertTokenizer.from_pretrained("ML/BGL/saved_model")
    model = BertForSequenceClassification.from_pretrained("ML/BGL/saved_model").to(device)

    df = pd.read_csv(f"logs/{filename}")
    texts = df["message"].tolist()

    dataset = TextDataset(texts, tokenizer)

    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    training_args = TrainingArguments(
        output_dir="./eval_results",
        per_device_eval_batch_size=32,
        do_train=False,
        do_predict=True,
        report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        tokenizer=tokenizer
    )

    predictions = trainer.predict(dataset)

    preds = np.argmax(predictions.predictions, axis=1)
    total_lines = len(preds)
    total_anomalies = int(len(preds) - preds.sum())
    probability = 1 - preds.sum() / total_lines
    print(probability)
    return {"probability": probability, "total_anomalies": total_anomalies, "total_lines": total_lines}
