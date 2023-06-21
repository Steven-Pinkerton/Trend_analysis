import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from rake_nltk import Rake
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import word_tokenize

# Named Entity Recognition
nlp = spacy.load('en_core_web_sm')

def extract_entities(text):
    doc = nlp(text)
    entities = [ent.text for ent in doc.ents]
    return entities

# TF-IDF
vectorizer = TfidfVectorizer(stop_words='english')

def extract_tfidf_keywords(text):
    tfidf_matrix = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.toarray()[0]
    sorted_indices = scores.argsort()[::-1]
    top_keywords = [feature_names[i] for i in sorted_indices[:10]]  # Adjust the number as needed
    return top_keywords

# RAKE
def extract_rake_keywords(text):
    rake = Rake()
    rake.extract_keywords_from_text(text)
    return rake.get_ranked_phrases()  # Returns all phrases ranked by score

# Lemmatization
def lemmatize_text(text):
    # Initialize the lemmatizer
    lemmatizer = WordNetLemmatizer()
    # Tokenize the text into words
    word_list = word_tokenize(text)
    # Lemmatize each word and join them back into a string
    lemmatized_output = ' '.join([lemmatizer.lemmatize(w) for w in word_list])
    return lemmatized_output

# Stemming
def stem_text(text):
    # Initialize the stemmer
    ps = PorterStemmer()
    # Tokenize the text into words
    word_list = word_tokenize(text)
    # Stem each word and join them back into a string
    stemmed_output = ' '.join([ps.stem(w) for w in word_list])
    return stemmed_output

# Driver function to call all the above functions
def extract_keywords(text):
    entities = extract_entities(text)
    tfidf_keywords = extract_tfidf_keywords(text)
    rake_keywords = extract_rake_keywords(text)
    print("Entities:", entities)
    print("TF-IDF Keywords:", tfidf_keywords)
    print("RAKE Keywords:", rake_keywords)

# Call the driver function
# extract_keywords(your_text_here)

def extract_keywords_from_db(conn, post_id):
    # Fetch the post content from the database
    text = fetch_post_content(conn, post_id)
    # Call the original extract_keywords function with the fetched text
    extract_keywords(text)

def fetch_post_content(conn, post_id):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT post_content 
        FROM posts 
        WHERE post_id = %s
    """, (post_id,))
    result = cursor.fetchone()
    if result is not None:
        return result[0]
    else:
        return None