from transformers import RobertaTokenizerFast, RobertaForSequenceClassification
from preprocessing import preprocess_text

from transformers import RobertaTokenizerFast, RobertaForSequenceClassification
from preprocessing import preprocess_text

# Initialize the model and tokenizer
tokenizer = RobertaTokenizerFast.from_pretrained('roberta-base')
model = RobertaForSequenceClassification.from_pretrained('roberta-base')

def infer_sentiment(text, timestamp):
    # Preprocess the text
    preprocessed_text = preprocess_text(text)

    # Rejoin tokens into a string. If using a different preprocessing method, you may need to adjust this
    preprocessed_string = ' '.join(preprocessed_text)

    # Tokenize the text
    inputs = tokenizer.encode_plus(
        preprocessed_string,
        return_tensors='pt',  # Return PyTorch tensors
        truncation=True,
        padding=True,
    )

    # Get the model's predictions
    outputs = model(**inputs)
    probs = outputs[0].softmax(1)

    # Convert the probabilities to a sentiment
    sentiment = 'positive' if probs[0][1] > probs[0][0] else 'negative'

    # Compute the sentiment score as the probability of the 'positive' class
    sentiment_score = probs[0][1].item()  # .item() to get the value as a Python float

    # Return the sentiment, its score, and the timestamp
    return sentiment, sentiment_score, timestamp