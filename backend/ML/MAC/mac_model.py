import pickle
import pandas as pd
from transformers import AutoTokenizer, AutoModel
import torch
from tqdm import tqdm
import numpy as np


def analyze(filename):
    with open('ML/MAC/mac_model.pkl', 'rb') as file:
        model_ = pickle.load(file)
    df = pd.read_csv(f"logs/{filename}")
    X = df["message"].tolist()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    torch.set_default_device(device)

    # This configures huggingface to not verify SSL
    # because of HTTPS errors when Paramon tried to test it on his Windows machine.
    from huggingface_hub import configure_http_backend
    import requests
    def backend_factory() -> requests.Session:
        session = requests.Session()
        session.verify = False
        return session

    configure_http_backend(backend_factory=backend_factory)
    MODEL_NAME = "bert-base-uncased"

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModel.from_pretrained(MODEL_NAME).to(device)
    model.eval()

    embeddings = []
    with torch.no_grad():
        for line in tqdm(X, desc="Analyzing"):
            inputs = tokenizer(line, return_tensors="pt", truncation=True, max_length=128, padding='max_length')
            outputs = model(**inputs)
            cls_embedding = outputs.last_hidden_state[:, 0, :].squeeze(0)
            embeddings.append(cls_embedding.cpu().numpy())

    embeddings = np.array(embeddings)

    scores = model_.decision_function(embeddings)
    threshold = 0  # predefined threshold (See 'mac_model_train.py')
    anomalies = [log for log, pred in zip(X, scores) if pred <= threshold]

    print(len(anomalies))
    print(len(X))
    return len(anomalies) / len(X)
