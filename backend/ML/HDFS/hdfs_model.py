import pickle
import pandas as pd


def analyze(filename, events_n):
    with open('ML/HDFS/hdfs_model.pkl', 'rb') as file:
        model = pickle.load(file)
    logs = pd.read_csv(f"logs/{filename}")
    X = logs[["EventId", "BlockID"]]
    X = X.groupby(["BlockID", "EventId"]).size().unstack(fill_value=0).reset_index()
    X.drop("BlockID", axis=1, inplace=True)
    events_ls = [f"E{i}" for i in range(1, events_n + 1)]
    for column in events_ls:
        if column not in X.columns:
            X[column] = 0

    X = X.reindex(sorted(X.columns, key=lambda x: int(x[1:])), axis=1)
    pred = model.predict(X)
    print(pred.sum() / len(pred))
    return pred.sum() / len(pred)
