from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import requests
import time
import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests

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
        self.processed_threads = {}  # Keep track of processed threads and their last post time

    def fetch_threads(self):
        response = requests.get(self.base_url)
        if response.status_code == 200:
            page_content = response.content
            soup = BeautifulSoup(page_content, 'html.parser')
            threads = soup.find_all('div', class_='thread')
            return threads
        else:
            print(f"Error: Status code {response.status_code}")
            return []
        
    def parse_post(self, post):
        post_number = post['id'].lstrip('p')
        post_text = post.find('blockquote', class_='postMessage').get_text()
        post_date = post.find('span', class_='dateTime')['data-utc']
        post_data = {
            'post_number': post_number,
            'post_text': post_text,
            'post_date': post_date,
        }
        return post_data
        
    def stream_posts(self, keywords, interval):
        try:
            threads = self.fetch_threads()
        except requests.exceptions.RequestException as e:
            print(f"Error: Failed to fetch threads. {e}")
            return []

        matching_posts = []
        for thread in threads:
            thread_url = thread.find('a', class_='replylink')['href']
            thread_url = self.base_url + thread_url

            last_post_time = self.processed_threads.get(thread_url)
            if last_post_time:
                newest_post = thread.find('div', class_='postContainer', order=-1)
                newest_post_time = newest_post.find('span', class_='dateTime')['data-utc']
                if newest_post_time <= last_post_time:
                    continue

            op = thread.find('div', class_='post op')
            op_text = op.find('blockquote', class_='postMessage').get_text()

            if any(keyword.lower() in op_text.lower() for keyword in keywords):
                self.processed_threads[thread_url] = None  # To be updated with the latest post's date
                
                response = requests.get(thread_url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    posts = soup.find_all('div', class_='postContainer')

                    for post in posts:
                        post_data = self.parse_post(post)
                        matching_posts.append(post_data)

                    self.processed_threads[thread_url] = post_data['post_date']  # Update with the latest post's date

        self.cleanup_threads(12 * 60 * 60)  # Remove threads with no new posts for 12 hours
        return matching_posts

    def cleanup_threads(self, inactive_threshold):
        current_time = datetime.datetime.now()
        for thread, last_post_time in list(self.processed_threads.items()):
            time_difference = current_time - datetime.datetime.fromtimestamp(last_post_time)
            if time_difference.total_seconds() > inactive_threshold:
                del self.processed_threads[thread]

class NeoGAF(SocialMediaSite):
    def __init__(self):
        self.base_url = 'https://www.neogaf.com/'
        self.processed_threads = {}  # Keep track of processed threads and their last post time

    def fetch_threads(self, forum):
        response = requests.get(self.base_url + forum)
        if response.status_code == 200:
            page_content = response.content
            soup = BeautifulSoup(page_content, 'html.parser')
            threads = soup.find_all('div', class_='structItem-title')
            return threads
        else:
            print(f"Error: Status code {response.status_code}")
            return []
        
    def parse_post(self, post):
        post_text = post.find('div', class_='bbWrapper').get_text()
        post_date = post.find('time')['datetime']
        post_data = {
            'post_text': post_text,
            'post_date': post_date,
        }
        return post_data

    def stream_posts(self, keywords, interval):
        try:
            threads = self.fetch_threads('forums/gaming-discussion.2/')
        except requests.exceptions.RequestException as e:
            print(f"Error: Failed to fetch threads. {e}")
            return []

        matching_posts = []
        for thread in threads:
            thread_url = thread.find('a', class_='structItem-title')['href']
            thread_url = self.base_url + thread_url

            last_post_time = self.processed_threads.get(thread_url)
            if last_post_time:
                newest_post = thread.find('article', class_='message', order=-1)
                newest_post_time = newest_post.find('time')['datetime']
                if newest_post_time <= last_post_time:
                    continue

            op = thread.find('article', class_='message')
            op_text = op.find('div', class_='bbWrapper').get_text()

            if any(keyword.lower() in op_text.lower() for keyword in keywords):
                self.processed_threads[thread_url] = None  # To be updated with the latest post's date
                
                response = requests.get(thread_url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    posts = soup.find_all('article', class_='message')

                    for post in posts:
                        post_data = self.parse_post(post)
                        matching_posts.append(post_data)

                    self.processed_threads[thread_url] = post_data['post_date']  # Update with the latest post's date

        self.cleanup_threads(12 * 60 * 60)  # Remove threads with no new posts for 12 hours
        return matching_posts

    def cleanup_threads(self, inactive_threshold):
        current_time = datetime.datetime.now()
        for thread, last_post_time in list(self.processed_threads.items()):
            time_difference = current_time - datetime.datetime.fromtimestamp(last_post_time)
            if time_difference.total_seconds() > inactive_threshold:
                del self.processed_threads[thread]

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