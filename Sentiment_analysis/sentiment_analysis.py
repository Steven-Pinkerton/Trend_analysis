import logging

def sentiment_analysis(post_id):
    try:
        # Get the sentiment, score and the timestamp of the post
        sentiment, score, timestamp = infer_sentiment(post_id)

        # Extract features and keywords from the post
        features = extract_features_from_db(post_id)
        keywords_dict = extract_keywords_from_db(post_id)
        # Merge the keywords into a single list
        keywords = merge_keywords(keywords_dict)

        # Combine all extracted data into a dictionary for further use
        sentiment_analysis_data = {
            "post_id": post_id,
            "sentiment": sentiment,
            "sentiment_score": score,
            "timestamp": timestamp,
            "features": features,
            "keywords": keywords
        }

        return sentiment_analysis_data
    except Exception as e:
        logging.error(f"Error while processing post {post_id}: {str(e)}")
        raise