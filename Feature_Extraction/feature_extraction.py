from datetime import datetime
from urllib.parse import urlsplit

class FeatureExtractor:
    def __init__(self, text, url=None, sentiment=None):
        self.text = text
        self.url = url
        self.sentiment = sentiment
        self.named_entities = {'ORG': [], 'PERSON': [], 'PRODUCT': []}
    
    def extract_company_name(self, preprocessed_content):
        # your function here
        pass
    
    def generate_extended_keywords(self, extracted_company):
        # your function here
        pass
    
    def capture_current_date(self):
        # Get the current date and time in UTC
        current_date = datetime.utcnow()
        return current_date

    def extract_named_entities(self):
        doc = nlp(self.text)
        for ent in doc.ents:
            if ent.label_ in self.named_entities:
                self.named_entities[ent.label_].append(ent.text)
        return self.named_entities

    def extract_source(self):
        if self.url:
            source = urlsplit(self.url).netloc
            return source.replace('www.', '')  # remove 'www.'
        else:
            return None

    def extract_features(self):
        # Call the extraction functions with the fetched text
        current_date = self.capture_current_date()
        named_entities = self.extract_named_entities()
        source = self.extract_source()

        features = {
            'current_date': current_date,
            'named_entities': named_entities,
            'source': source,
            'sentiment': self.sentiment
        }

        return features