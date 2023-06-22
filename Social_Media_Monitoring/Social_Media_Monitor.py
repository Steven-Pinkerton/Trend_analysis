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
        self.processed_threads = set()  # Keep track of processed threads

    def fetch_threads(self):
        # Fetch the HTML of the page
        response = requests.get(self.base_url)
        
        # If the request was successful, the status code will be 200
        if response.status_code == 200:
            # Get the content of the response
            page_content = response.content
            
            # Create a BeautifulSoup object and specify the parser
            soup = BeautifulSoup(page_content, 'html.parser')
            
            # Find all the threads on the page
            threads = soup.find_all('div', class_='thread')
            
            return threads
        
        else:
            print(f"Error: Status code {response.status_code}")
            return []
        
        
    def parse_post(self, post):
        # Extract post number, text, and date from post
        post_number = post['id'].lstrip('p')
        post_text = post.find('blockquote', class_='postMessage').get_text()
        post_date = post.find('span', class_='dateTime')['data-utc']

        # Create a dictionary containing post data
        post_data = {
            'post_number': post_number,
            'post_text': post_text,
            'post_date': post_date,
        }

        return post_data
        
    def stream_posts(self, keywords, interval):
        # Fetch the threads
        try:
            threads = self.fetch_threads()
        except requests.exceptions.RequestException as e:
            print(f"Error: Failed to fetch threads. {e}")
            return []

        matching_posts = []
        for thread in threads:
            # Get the URL of the thread
            thread_url = thread.find('a', class_='replylink')['href']
            thread_url = self.base_url + thread_url

            # Skip this thread if it has already been processed
            if thread_url in self.processed_threads:
                continue

            # Get the OP of the thread
            op = thread.find('div', class_='post op')
            op_text = op.find('blockquote', class_='postMessage').get_text()

            # If the OP contains any of the keywords, fetch the posts in the thread
            if any(keyword.lower() in op_text.lower() for keyword in keywords):
                self.processed_threads.add(thread_url)  # Mark this thread as processed
                
                # Fetch the HTML of the thread
                response = requests.get(thread_url)
                if response.status_code == 200:
                    # Create a BeautifulSoup object and specify the parser
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Find all the posts in the thread
                    posts = soup.find_all('div', class_='postContainer')

                    for post in posts:
                        post_data = self.parse_post(post)
                        matching_posts.append(post_data)

        return matching_posts


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