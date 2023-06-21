from bs4 import BeautifulSoup
import html
import nltk
import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

def clean_text(text):
    text = html.unescape(text)  # Unescape HTML entities
    text = BeautifulSoup(text, "html.parser").get_text()  # Remove HTML tags
    text = text.lower()  # Lowercasing
    text = re.sub(r'http[s]?://\S+', '', text)  # URL removal
    text = text.translate(str.maketrans('', '', string.punctuation))  # Punctuation removal
    return text

def tokenize(text):
    return word_tokenize(text)

def remove_stopwords(tokens):
    stop_words = set(stopwords.words('english'))
    return [token for token in tokens if token not in stop_words]

def lemmatize(tokens):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token) for token in tokens]

def preprocess_text(text):
    text = clean_text(text)
    tokens = tokenize(text)
    tokens = remove_stopwords(tokens)
    tokens = lemmatize(tokens)
    # Join the tokens back together
    text = " ".join(tokens)
    return text