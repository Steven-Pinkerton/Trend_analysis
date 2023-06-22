from abc import ABC, abstractmethod

class NewsSite(ABC):
    @abstractmethod
    def fetch_articles(self, keywords):
        pass


class BBCNews(NewsSite):
    def fetch_articles(self, keywords):
        # Implementation for BBC News goes here.
        pass


class CNNNews(NewsSite):
    def fetch_articles(self, keywords):
        # Implementation for CNN News goes here.
        pass


class NewsMonitor:
    def __init__(self, sites):
        self.sites = sites

    def monitor(self, keywords):
        news_data = []
        for site in self.sites:
            data = site.fetch_articles(keywords)
            news_data.append(data)
        
        return news_data