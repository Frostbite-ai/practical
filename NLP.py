import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download the VADER lexicon
nltk.download("vader_lexicon")

# Initialize the SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(text):
    sentiment = analyzer.polarity_scores(text)
    compound_score = sentiment["compound"]
    if compound_score >= 0.05:
        return "Positive"
    elif compound_score <= -0.05:
        return "Negative"
    else:
        return "Neutral"


if __name__ == "__main__":
    text = "I love this product! It's amazing."
    sentiment = analyze_sentiment(text)
    print(f"Sentiment: {sentiment}")

    text = "I hate this. It's terrible."
    sentiment = analyze_sentiment(text)
    print(f"Sentiment: {sentiment}")

    text = "This is an average item."
    sentiment = analyze_sentiment(text)
    print(f"Sentiment: {sentiment}")
