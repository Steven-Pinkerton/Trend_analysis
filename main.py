import datetime
import keyword
import time
from Database_Code.db_management import insert_data
from feature_extraction import FeatureExtractor
from sentiment_analysis import SentimentAnalyzer
from stock_data_acquisition import get_stock_data
from stock_data_preprocessing import preprocess_stock_data
from trend_analysis import TrendAnalyzer
from correlation_analysis import CorrelationAnalyzer
from data_integration import DataIntegrator
from dependency_parser import parse_sentence
from fuzzy_matching import get_fuzzy_matches, is_fuzzy_match
from keyword_generator import generate_extended_keywords
from regex_patterns import generate_patterns, contains_keywords
from scraper_database import create_connection, create_table, insert_thread, update_thread, delete_thread

def main(api_key, keywords, subreddit, interval):
    try:
        sentiment_analyzer = SentimentAnalyzer()
        trend_analyzer = TrendAnalyzer()
        fourchan = FourChan()
        neogaf = NeoGAF()
        resetera = ResetEra()
        reddit = Reddit(subreddit)

        conn = psycopg2.connect(
            host="your_host",
            database="your_database",
            user="your_user",
            password="your_password"
        )
        create_tables(conn)

        while True:
            social_media_data_4chan = fourchan.stream_posts(keywords, interval)
            social_media_data_neogaf = neogaf.stream_posts(keywords, interval)
            social_media_data_resetera = resetera.stream_posts(keywords, interval)
            social_media_data_reddit = reddit.stream_posts(keywords, interval)

            for data in (social_media_data_4chan, social_media_data_neogaf, social_media_data_resetera, social_media_data_reddit):
                for post_data in data:
                    sentiment_score = sentiment_analyzer.analyze(post_data['post_text'])
                    post_data['sentiment_score'] = sentiment_score
                    insert_data(conn, 'SocialMediaPosts', post_data)

            symbols = extract_company_symbols(social_media_data_4chan + social_media_data_neogaf + social_media_data_resetera + social_media_data_reddit)
            stock_data = get_stock_data(symbols, api_key=api_key)
            preprocessed_stock_data = preprocess_stock_data(stock_data)

            data_integrator = DataIntegrator(preprocessed_stock_data, features)
            integrated_data = data_integrator.integrate_data()

            trends = trend_analyzer.analyze(integrated_data)
            correlation_analyzer = CorrelationAnalyzer(integrated_data)
            correlations = correlation_analyzer.calculate_rolling_correlation()

            if correlations < correlation_threshold or trend_slope < trend_slope_threshold:
                print("Termination condition met. Stopping data analysis.")
                break

            send_to_haskell(trends, correlations)

            print(f"[{datetime.now()}] Sent trends and correlations to Haskell program. Sleeping for {interval} seconds.")
            time.sleep(interval)

    except psycopg2.Error as e:
        print(f"Error: Failed to connect to the database. {e}")
        return
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to fetch threads. {e}")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return
    finally:
        conn.close()

if __name__ == "__main__":
    api_key = "your_alpha_vantage_api_key"
    keywords = ["your_keywords"]
    subreddit = "your_subreddit"
    interval = 60 

    main(api_key, keywords, subreddit, interval)