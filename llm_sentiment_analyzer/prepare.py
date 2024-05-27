import pandas as pd
import numpy as np
from llm import get_sentiment
from utils import preprocess_text
from sklearn.preprocessing import LabelEncoder


def filter_sentiment_rows(df):
    return df[df["sentiment"].isin(["Positive", "Neutral", "Negative"])]


def preprocess_df(df):
    df = df.dropna(subset=["tweet_content", "sentiment"])
    df.tweet_content = df.tweet_content.apply(preprocess_text)
    df = df.dropna(subset=["tweet_content", "sentiment"])
    return filter_sentiment_rows(df)


def get_features_label(df, label_encoder=None):
    scores = []

    if not label_encoder:
        label_encoder = LabelEncoder()
        sentiments_label = label_encoder.fit_transform(
            df["sentiment"]
        )  # {{'Negative': 0, 'Neutral': 1, 'Positive': 2}}
        np.save("outputs/labels/labels.npy", label_encoder.classes_)
    else:
        sentiments_label = label_encoder.transform(df["sentiment"])

    for _, row in df.iterrows():
        content = preprocess_text(row["tweet_content"])
        score = get_sentiment(content)
        scores.append(score)
    return scores, sentiments_label


if __name__ == "__main__":
    train_df = pd.read_csv("data/train/twitter_training.csv")

    filtered_df = filter_sentiment_rows(train_df)
    print(filtered_df["sentiment"].unique())
