"""
Twitter Data Collector Module
Collects tweets based on keywords and hashtags from specified regions
"""

import tweepy
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
import json
from dotenv import load_dotenv


class TwitterCollector:
    """Collects tweets using Twitter API v2"""

    def __init__(self):
        """Initialize Twitter API client"""
        load_dotenv()

        # Get credentials from environment
        bearer_token = os.getenv('TWITTER_BEARER_TOKEN')

        if not bearer_token:
            raise ValueError("Twitter API credentials not found. Please check your .env file")

        # Initialize Tweepy client with API v2
        self.client = tweepy.Client(
            bearer_token=bearer_token,
            wait_on_rate_limit=True
        )

    def build_query(self, keywords: List[str], hashtags: List[str], max_terms: int = 10) -> str:
        """
        Build Twitter search query from keywords and hashtags

        Args:
            keywords: List of keywords to search
            hashtags: List of hashtags to search
            max_terms: Maximum number of terms to include (Twitter has query length limits)

        Returns:
            Formatted query string
        """
        # Combine and limit terms
        all_terms = keywords[:max_terms//2] + hashtags[:max_terms//2]

        # Build OR query
        query_parts = []
        for term in all_terms:
            if term.startswith('#'):
                query_parts.append(term)
            else:
                query_parts.append(f'"{term}"')

        query = ' OR '.join(query_parts)

        # Add language filter and exclude retweets
        query += ' -is:retweet lang:en'

        return query

    def collect_tweets(self, config: Dict[str, Any], max_results: int = 100) -> List[Dict[str, Any]]:
        """
        Collect tweets based on configuration

        Args:
            config: Configuration dictionary with keywords and hashtags
            max_results: Maximum number of tweets to collect

        Returns:
            List of tweet data dictionaries
        """
        query = self.build_query(config['keywords'], config['hashtags'])

        print(f"Searching for: {query}")
        print(f"Collecting up to {max_results} tweets...")

        tweets_data = []

        try:
            # Search recent tweets (last 7 days)
            tweets = self.client.search_recent_tweets(
                query=query,
                max_results=min(max_results, 100),  # API limit is 100 per request
                tweet_fields=['created_at', 'geo', 'public_metrics', 'author_id', 'entities'],
                expansions=['author_id', 'geo.place_id'],
                place_fields=['full_name', 'country', 'geo', 'place_type']
            )

            if not tweets.data:
                print("No tweets found matching the criteria")
                return tweets_data

            # Build user lookup dict
            users = {}
            if tweets.includes and 'users' in tweets.includes:
                for user in tweets.includes['users']:
                    users[user.id] = user.username

            # Build place lookup dict
            places = {}
            if tweets.includes and 'places' in tweets.includes:
                for place in tweets.includes['places']:
                    places[place.id] = place

            # Process tweets
            for tweet in tweets.data:
                tweet_info = {
                    'id': tweet.id,
                    'text': tweet.text,
                    'created_at': str(tweet.created_at),
                    'author_id': tweet.author_id,
                    'author_username': users.get(tweet.author_id, 'unknown'),
                    'likes': tweet.public_metrics['like_count'],
                    'retweets': tweet.public_metrics['retweet_count'],
                    'replies': tweet.public_metrics['reply_count'],
                    'geo': None,
                    'place': None,
                    'coordinates': None
                }

                # Extract geo information if available
                if hasattr(tweet, 'geo') and tweet.geo:
                    if 'place_id' in tweet.geo:
                        place = places.get(tweet.geo['place_id'])
                        if place:
                            tweet_info['place'] = {
                                'name': place.full_name,
                                'country': place.country if hasattr(place, 'country') else None,
                                'place_type': place.place_type if hasattr(place, 'place_type') else None
                            }

                            # Extract coordinates from place
                            if hasattr(place, 'geo') and place.geo:
                                if 'bbox' in place.geo:
                                    bbox = place.geo['bbox']
                                    # Calculate center of bounding box
                                    tweet_info['coordinates'] = {
                                        'lat': (bbox[1] + bbox[3]) / 2,
                                        'lon': (bbox[0] + bbox[2]) / 2,
                                        'type': 'bbox_center'
                                    }

                tweets_data.append(tweet_info)

            print(f"Collected {len(tweets_data)} tweets")

        except tweepy.TweepyException as e:
            print(f"Error collecting tweets: {e}")
            print("Note: Twitter API v2 requires elevated access for full functionality")

        return tweets_data

    def save_tweets(self, tweets: List[Dict[str, Any]], filename: str):
        """Save tweets to JSON file"""
        os.makedirs('data', exist_ok=True)
        filepath = os.path.join('data', filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(tweets, f, indent=2, ensure_ascii=False)

        print(f"Saved {len(tweets)} tweets to {filepath}")
