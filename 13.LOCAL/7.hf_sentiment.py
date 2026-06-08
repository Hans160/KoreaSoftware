# pip install transformers
from transformers import pipeline

sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")

result = sentiment_analyzer("I'm hungry")
print(result)

result = sentiment_analyzer("I'm tired")
print(result)

result = sentiment_analyzer("I'm happy")
print(result[0]['label'])