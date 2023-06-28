from abc import ABC, abstractmethod

class NewsSite(ABC):
    @abstractmethod
    def fetch_articles(self, keywords):
        pass


class EuroGamer(NewsSite):
    def fetch_articles(self, keywords):
        # Implementation for EuroGamer goes here.
        pass


class GamesIndustry(NewsSite):
    def fetch_articles(self, keywords):
        # Implementation for GamesIndustry goes here.
        pass

# Repeat similar class definitions for GamesSpot, GameSutra, IGN, Kotaku, PCGamer, PolyGone, RPS, and VentureBeat

class NewsMonitor:
    def __init__(self, sites):
        self.sites = sites

    def monitor(self, keywords):
        news_data = []
        for site in self.sites:
            data = site.fetch_articles(keywords)
            news_data.append(data)
        
        return news_data