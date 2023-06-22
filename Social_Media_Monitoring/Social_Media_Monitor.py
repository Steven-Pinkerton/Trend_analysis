from abc import ABC, abstractmethod
import time

class SocialMediaSite(ABC):
    @abstractmethod
    def stream_posts(self, keywords, interval):
        pass


class Twitter(SocialMediaSite):
    def stream_posts(self, keywords, interval):
        # Implementation for Twitter goes here.
        pass


class Reddit(SocialMediaSite):
    def stream_posts(self, keywords, interval):
        # Implementation for Reddit goes here.
        pass


class SocialMediaMonitor:
    def __init__(self, sites):
        self.sites = sites

    def monitor(self, keywords, interval):
        social_media_data = []
        for site in self.sites:
            data = site.stream_posts(keywords, interval)
            social_media_data.append(data)
        
        return social_media_data


if __name__ == "__main__":
    twitter = Twitter()
    reddit = Reddit()
    monitor = SocialMediaMonitor([twitter, reddit])
    
    keywords = ["Bitcoin", "Ethereum"]  # for example
    interval = 60  # in seconds

    while True:
        data = monitor.monitor(keywords, interval)
        # TODO: process data
        time.sleep(interval)