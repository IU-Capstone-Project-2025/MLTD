from sklearn.metrics import classification_report
import torch
from bgl_parser import parse_file
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from torch.utils.data import Dataset
from tqdm import tqdm
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments


df = parse_file("BGL.log", for_train=True)
df["prefix"] = df["prefix"].apply(lambda x: "Anomalous" if x != "-" else "Normal")

# here we take only 20% of initial dataset because it has very large size (4.7kk)
sample_df, _ = train_test_split(df,
                                 stratify=df["prefix"],
                                 train_size=0.2,
                                 random_state=42)

X_train, X_test, y_train, y_test = train_test_split(sample_df["message"], sample_df["prefix"], test_size=0.2)


model_name = "bert-base-uncased"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(
    model_name,
    num_labels=2
)


def batch_tokenize(texts, batch_size=1000):
    encodings = {
        'input_ids': [],
        'attention_mask': []
    }

    for i in tqdm(range(0, len(texts), batch_size), desc="Tokenizing"):
        batch = texts[i:i + batch_size]
        batch_encodings = tokenizer(
            batch,
            truncation=True,
            padding='max_length',
            max_length=128,
            return_tensors="pt"
        )
        encodings['input_ids'].append(batch_encodings['input_ids'])
        encodings['attention_mask'].append(batch_encodings['attention_mask'])

    return {
        'input_ids': torch.cat(encodings['input_ids']),
        'attention_mask': torch.cat(encodings['attention_mask'])
    }


X_train_list = X_train.tolist() if hasattr(X_train, 'tolist') else X_train
X_test_list = X_test.tolist() if hasattr(X_test, 'tolist') else X_test

train_encodings = batch_tokenize(X_train_list)
test_encodings = batch_tokenize(X_test_list)

label_encoder = LabelEncoder()
y_train_numeric = label_encoder.fit_transform(y_train)
y_test_numeric = label_encoder.transform(y_test)

class LogsDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {
            key: torch.tensor(val[idx])
            for key, val in self.encodings.items()
        }
        item["labels"] = torch.tensor(int(self.labels[idx]))
        return item

    def __len__(self):
        return len(self.labels)


train_dataset = LogsDataset(train_encodings, y_train_numeric)
test_dataset = LogsDataset(test_encodings, y_test_numeric)


training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=16,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
    eval_strategy="epoch"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset
)

trainer.train()

predictions = trainer.predict(test_dataset)
predicted_labels = predictions.predictions.argmax(axis=1)

print(classification_report(y_test_numeric, predicted_labels))

model.save_pretrained("ML/BGL/saved_model")
tokenizer.save_pretrained("ML?BGL/saved_model")