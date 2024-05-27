import pickle
import numpy as np
import streamlit as st
from llm import get_sentiment
from utils import preprocess_text
from sklearn.preprocessing import LabelEncoder

st.title("Sentiment Analyzer")

with open("outputs/models/model.pkl", "rb") as f:
    model = pickle.load(f)

label_encoder = LabelEncoder()
label_encoder.classes_ = np.load("outputs/labels/labels.npy", allow_pickle=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.markdown(
    """
    <style>
        .st-emotion-cache-janbn0 {
            flex-direction: row-reverse;
            text-align: right;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

if prompt := st.chat_input("Give me a text to analyse"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    preprocessed_text = preprocess_text(prompt)
    sentiment_score = get_sentiment(preprocess_text(prompt))
    feature = np.array(sentiment_score).reshape(1, -1)
    prediction = model.predict(feature)[0]

    response = label_encoder.classes_[prediction]

    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
