import numpy as np
import torch
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModel

from ssh_parser import parse_file
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import pickle

# df = parse_file("SSH.log", for_train=True)
# X = df["message"].tolist()
#
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#
#
# MODEL_NAME = "bert-base-uncased"
#
# tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
# model = AutoModel.from_pretrained(MODEL_NAME).to(device)
# model.eval()
#
#
# def get_embeddings(logs):
#     embeddings = []
#     with torch.no_grad():
#         for line in tqdm(logs, desc="Analyzing"):
#             inputs = tokenizer(line, return_tensors="pt", truncation=True, max_length=128, padding='max_length')
#             outputs = model(**inputs)
#             cls_embedding = outputs.last_hidden_state[:, 0, :].squeeze(0)
#             embeddings.append(cls_embedding.numpy())
#     return np.array(embeddings)
#
# embeddings = get_embeddings(X)
# np.save("ssh_log_embeddings.npy", embeddings)


embeddings = np.load("ssh_log_embeddings.npy") # already completed embeddings
model_ = IsolationForest(contamination="auto", random_state=42)
model_.fit(embeddings)


scores = model_.decision_function(embeddings)
plt.hist(scores, bins=100)

# Now we will find the threshold for anomalies according to the graph.
threshold = -0.05
plt.axvline(x=threshold, color='r')
plt.show()

with open('ssh_model.pkl', 'wb') as f:
    pickle.dump(model_, f)