import re
import numpy as np


def preprocess_text(text):
    filtered_text = re.sub("[^A-Za-z0-9]+", " ", text).lower().strip()
    if not filtered_text or text == np.nan or len(filtered_text.split()) == 1:
        return np.nan
    return filtered_text


def convert_to_scores(probabilities):
    scores = [p / sum(probabilities) for p in probabilities]
    return scores


if __name__ == "__main__":
    print(
        preprocess_text(
            "Let no elim go unnoticed. . . . NVIDIA Highlights automatically records your best moments in @FortniteGame on GFN!. . Share them with"
        )
    )

    print(convert_to_scores([0.2, 0.1, 0.7]))
