import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix
import pickle

df = pd.read_csv("./log_data/HDFS_v1/preprocessed/hybrid_training_dataset.csv")
X, y = df.drop("Label", axis=1), df["Label"].apply(lambda x: {"Success": 0, "Fail": 1}[x])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = DecisionTreeClassifier()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall:", recall_score(y_test, y_pred))
print("F1 score:", f1_score(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))

with open('./HDFS/hdfs_model.pkl', 'wb') as file:
    pickle.dump(model, file)
