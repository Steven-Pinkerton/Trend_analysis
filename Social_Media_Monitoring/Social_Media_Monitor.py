from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import requests
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


class FourChan(SocialMediaSite):
    def __init__(self):
        self.base_url = 'https://boards.4chan.org/v/'

    def stream_posts(self, keywords, interval):
        # Fetch the HTML of the page
        response = requests.get(self.base_url)
        
        # If the request was successful, the status code will be 200
        if response.status_code == 200:
            # Get the content of the response
            page_content = response.content
            
            # Create a BeautifulSoup object and specify the parser
            soup = BeautifulSoup(page_content, 'html.parser')
            
            # Find all the posts on the page
            posts = soup.find_all('div', class_='postContainer')
            
            # Loop through each post and check if it contains any of the keywords
            matching_posts = []
            for post in posts:
                post_text = post.get_text()
                if any(keyword.lower() in post_text.lower() for keyword in keywords):
                    matching_posts.append(post)
            
            return matching_posts
        
        else:
            print(f"Error: Status code {response.status_code}")
            return []


class NeoGAF(SocialMediaSite):
    def stream_posts(self, keywords, interval):
        # Implementation for NeoGAF goes here.
        pass


class ResetEra(SocialMediaSite):
    def stream_posts(self, keywords, interval):
        # Implementation for ResetEra goes here.
        pass


class GameFAQs(SocialMediaSite):
    def stream_posts(self, keywords, interval):
        # Implementation for GameFAQs goes here.
        pass


class SteamCommunity(SocialMediaSite):
    def stream_posts(self, keywords, interval):
        # Implementation for Steam Community goes here.
        pass


class StockTwits(SocialMediaSite):
    def stream_posts(self, keywords, interval):
        # Implementation for StockTwits goes here.
        pass


class LinkedIn(SocialMediaSite):
    def stream_posts(self, keywords, interval):
        # Implementation for LinkedIn goes here.
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
    fourchan = FourChan()
    neogaf = NeoGAF()
    resetera = ResetEra()
    gamefaqs = GameFAQs()
    steam_community = SteamCommunity()
    stocktwits = StockTwits()
    linkedin = LinkedIn()

    monitor = SocialMediaMonitor([twitter, reddit, fourchan, neogaf, resetera, gamefaqs, steam_community, stocktwits, linkedin])
    
    keywords = ["scandal", "game company"]  # for example
    interval = 60  # in seconds

    while True:
        data = monitor.monitor(keywords, interval)
        # TODO: process data
        time.sleep(interval)