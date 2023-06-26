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
    def __init__(self, subreddit, username, password):
        self.base_url = f'https://www.reddit.com/r/{subreddit}/'
        self.processed_threads = {}  # Keep track of processed threads and their last post time

        self.driver = webdriver.Firefox()  # Or you could use Chrome or any other browser

        # Reddit login
        self.driver.get("https://www.reddit.com/login/")
        time.sleep(2)  # Wait for the page to load
        self.driver.find_element_by_id("loginUsername").send_keys(username)
        self.driver.find_element_by_id("loginPassword").send_keys(password)
        self.driver.find_element_by_class_name("AnimatedForm__submitButton").click()
        time.sleep(2)  # Wait for login to complete

    def fetch_threads(self):
        self.driver.get(self.base_url)
        time.sleep(2)  # Wait for the page to load
        threads = self.driver.find_elements_by_class_name("_1poyrkZ7g36PawDueRza-J")
        return threads

    def process_thread(self, thread):
        # Process a single thread to extract useful information
        try:
            title = thread.find_element_by_class_name("_eYtD2XCVieq6emjKBH3m").text
            link = thread.find_element_by_class_name("SQnoC3ObvgnGjWt90zD9Z_").get_attribute('href')
            comments = thread.find_element_by_class_name("FHCV02u6Cp2zYL0fhQPsO").text

            return {'title': title, 'link': link, 'comments': comments}
        except Exception as e:
            print(f"Error processing thread: {e}")
            return {}

    def stream_posts(self, keywords, interval):
        seen_post_ids = set()
        while True:
            hot_posts = self.reddit.subreddit(self.subreddit).hot(limit=100)
            rising_posts = self.reddit.subreddit(self.subreddit).rising(limit=100)

            for post in itertools.chain(hot_posts, rising_posts):
                # If we've already seen this post, skip it
                if post.id in seen_post_ids:
                    continue

                # Add the post's ID to our set of seen posts
                seen_post_ids.add(post.id)

                # Check if the post contains any of the keywords
                if any(keyword.lower() in post.title.lower() for keyword in keywords):
                    post_data = {
                        'post_id': post.id,
                        'title': post.title,
                        'url': post.url,
                        'created_utc': post.created_utc
                    }
                    yield post_data

            time.sleep(interval)

    def cleanup_threads(self, inactive_threshold):
        current_time = datetime.datetime.now()
        for thread, last_post_time in list(self.processed_threads.items()):
            time_difference = current_time - datetime.datetime.fromtimestamp(last_post_time)
            if time_difference.total_seconds() > inactive_threshold:
                del self.processed_threads[thread]

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
    def __init__(self):
        self.base_url = 'https://www.resetera.com/'
        self.processed_threads = {}  # Keep track of processed threads and their last post time

    def fetch_threads(self):
        response = requests.get(self.base_url)
        if response.status_code == 200:
            page_content = response.content
            soup = BeautifulSoup(page_content, 'html.parser')
            threads = soup.find_all('div', class_='structItem structItem--thread')
            return threads
        else:
            print(f"Error: Status code {response.status_code}")
            return []
        
    def parse_post(self, post):
        user_id = post.get('data-author')
        post_id = post.get('data-content')

        post_text = post.find('div', class_='bbWrapper').get_text()

        post_date_str = post.find('time', class_='u-dt')['datetime']  
        post_date = dateutil.parser.parse(post_date_str)  # parse the datetime string into a datetime object

        post_data = {
            'user_id': user_id,
            'post_id': post_id,
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
            thread_url = thread.find('div', class_='structItem-title').find('a').get('href')
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