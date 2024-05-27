import json
import pickle
import prepare
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report

with open("outputs/models/model.pkl", "rb") as f:
    model = pickle.load(f)

label_encoder = LabelEncoder()
label_encoder.classes_ = np.load("outputs/labels/labels.npy", allow_pickle=True)

train_df = pd.read_csv("data/train/twitter_training.csv")
filtered_train_df = prepare.preprocess_df(train_df)
sample_df = filtered_train_df.groupby("sentiment").sample(n=100).sample(frac=1)
sample_df.to_csv("outputs/samples/test.csv")
scores, labels = prepare.get_features_label(sample_df, label_encoder)
X = np.array(scores).reshape(-1, 1)

predictions = model.predict(X)
results = classification_report(
    labels, predictions, target_names=label_encoder.classes_, output_dict=True
)

with open("outputs/results/metrics.json", "w") as f:
    json.dump(results, f, indent=4)
