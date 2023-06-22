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

def main(url, content, api_key, board, interval):
    try:
        # Instantiate all necessary objects
        feature_extractor = FeatureExtractor(content, url)
        sentiment_analyzer = SentimentAnalyzer()
        trend_analyzer = TrendAnalyzer()
        fourchan = FourChan()

        # Database connection
        conn = psycopg2.connect(
            host="your_host",
            database="your_database",
            user="your_user",
            password="your_password"
        )
        create_tables(conn)

        while True:
            # Extract features
            features = feature_extractor.extract_features()

            # Fetch and preprocess stock data
            symbols = feature_extractor.extract_company(content)
            stock_data = get_stock_data(symbols, api_key=api_key)
            preprocessed_stock_data = preprocess_stock_data(stock_data)

            # Perform sentiment analysis on the news article
            sentiment_score = sentiment_analyzer.analyze(content)

            # Extract necessary features from the news article
            features = feature_extractor.extract(content)
            features['sentiment_score'] = sentiment_score

            # Fetch social media data from 4chan
            social_media_data = fourchan.stream_posts(keyword, interval)
            for post_data in social_media_data:
                # Insert social media data into the database
                insert_data(conn, 'SocialMediaPosts', post_data)

            # Integrate stock data with sentiment data and features
            data_integrator = DataIntegrator(preprocessed_stock_data, features)
            integrated_data = data_integrator.integrate_data()

            # Perform trend analysis on the integrated data
            trends = trend_analyzer.analyze(integrated_data)

            # Instantiate CorrelationAnalyzer with the integrated data
            correlation_analyzer = CorrelationAnalyzer(integrated_data)

            # Perform correlation analysis on the integrated data
            correlations = correlation_analyzer.calculate_rolling_correlation()

            # Check if the correlation has stopped or trend has fallen drastically
            if correlations < correlation_threshold or trend_slope < trend_slope_threshold:
                print("Termination condition met. Stopping data analysis.")
                break

            # Send the trends and correlations to the Haskell program
            # (WORK ON THIS PART)
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
        # Always ensure the connection is closed
        conn.close()

if __name__ == "__main__":
    url = "your_article_url"
    content = "your_article_content"
    api_key = "your_alpha_vantage_api_key"
    board = "your_board"
    interval = 60  # scrape interval in seconds

    main(url, content, api_key, board, interval)