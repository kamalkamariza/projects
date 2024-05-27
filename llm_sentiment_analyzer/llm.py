from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def get_sentiment(text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """
                You will be provided with a text and your task is to classify its sentiment specifically in integer from range 0 to 100.
                0 is negative, 100 is positive. 
                Only return an integer.
                If unable to classify the sentiment due to any reason such as not enough context or no text provided, return 50 to indicate Neutral
                """,
            },
            {"role": "user", "content": text},
        ],
        temperature=0.5,
        max_tokens=64,
        top_p=1,
    )

    return int(response.choices[0].message.content)


if __name__ == "__main__":
    score = get_sentiment("I really Love KFC")
    print(score)
