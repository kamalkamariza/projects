import os
import pickle
import prepare
import pandas as pd
import numpy as np
from sklearn.naive_bayes import GaussianNB

os.makedirs("outputs/labels", exist_ok=True)
os.makedirs("outputs/models", exist_ok=True)
os.makedirs("outputs/samples", exist_ok=True)

train_df = pd.read_csv("data/train/twitter_training.csv")
filtered_train_df = prepare.preprocess_df(train_df)
sample_df = filtered_train_df.groupby("sentiment").sample(n=100).sample(frac=1)
sample_df.to_csv("outputs/samples/train.csv")
scores, labels = prepare.get_features_label(sample_df)
X = np.array(scores).reshape(-1, 1)

model = GaussianNB()
model.fit(X, labels)

with open("outputs/models/model.pkl", "wb") as f:
    pickle.dump(model, f)
