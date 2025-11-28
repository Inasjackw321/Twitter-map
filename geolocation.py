"""
Geolocation Module
Extracts and geocodes location information from tweets
"""

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import re
import time
from typing import Dict, List, Any, Optional, Tuple
import json


class GeolocatorService:
    """Handles geolocation extraction and geocoding"""

    def __init__(self):
        """Initialize geocoder"""
        self.geolocator = Nominatim(user_agent="twitter_conflict_mapper")
        self.cache = {}  # Cache for geocoded locations

    def extract_location_from_text(self, text: str, config_keywords: List[str]) -> List[str]:
        """
        Extract potential location mentions from tweet text

        Args:
            text: Tweet text
            config_keywords: Keywords from configuration (likely locations)

        Returns:
            List of potential location strings
        """
        locations = []

        # Check for config keywords (cities, regions mentioned in config)
        for keyword in config_keywords:
            if keyword.lower() in text.lower():
                locations.append(keyword)

        # Extract capitalized multi-word phrases (potential place names)
        # Pattern matches sequences like "New York" or "Tel Aviv"
        capitalized_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b'
        matches = re.findall(capitalized_pattern, text)
        locations.extend(matches)

        return list(set(locations))  # Remove duplicates

    def geocode_location(self, location: str, bounds: Optional[Dict[str, float]] = None) -> Optional[Dict[str, float]]:
        """
        Geocode a location string to coordinates

        Args:
            location: Location string to geocode
            bounds: Optional geographic bounds to constrain search

        Returns:
            Dictionary with lat/lon or None
        """
        # Check cache first
        cache_key = f"{location}_{str(bounds)}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        try:
            # Add delay to respect rate limits
            time.sleep(1)

            # Build viewbox parameter if bounds provided
            viewbox = None
            if bounds:
                viewbox = [
                    (bounds['min_lat'], bounds['min_lon']),
                    (bounds['max_lat'], bounds['max_lon'])
                ]

            # Geocode
            location_data = self.geolocator.geocode(
                location,
                exactly_one=True,
                timeout=10,
                bounded=True if viewbox else False,
                viewbox=viewbox[0] + viewbox[1] if viewbox else None
            )

            if location_data:
                result = {
                    'lat': location_data.latitude,
                    'lon': location_data.longitude,
                    'display_name': location_data.address
                }
                self.cache[cache_key] = result
                return result

        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"Geocoding error for '{location}': {e}")
        except Exception as e:
            print(f"Unexpected error geocoding '{location}': {e}")

        return None

    def process_tweets_geolocation(self, tweets: List[Dict[str, Any]], config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Process tweets to extract and enhance geolocation data

        Args:
            tweets: List of tweet dictionaries
            config: Configuration with keywords and geographic bounds

        Returns:
            Enhanced tweet list with geolocation data
        """
        enhanced_tweets = []
        bounds = config.get('geographic_bounds')

        print(f"Processing geolocation for {len(tweets)} tweets...")

        for i, tweet in enumerate(tweets):
            enhanced_tweet = tweet.copy()

            # Skip if already has valid coordinates
            if tweet.get('coordinates'):
                enhanced_tweets.append(enhanced_tweet)
                continue

            # Try to extract location from text
            locations = self.extract_location_from_text(
                tweet['text'],
                config.get('keywords', [])
            )

            # Try to geocode extracted locations
            for location in locations:
                coords = self.geocode_location(location, bounds)
                if coords:
                    # Check if coordinates are within bounds
                    if bounds:
                        if (bounds['min_lat'] <= coords['lat'] <= bounds['max_lat'] and
                            bounds['min_lon'] <= coords['lon'] <= bounds['max_lon']):
                            enhanced_tweet['coordinates'] = {
                                'lat': coords['lat'],
                                'lon': coords['lon'],
                                'type': 'text_extraction'
                            }
                            enhanced_tweet['extracted_location'] = location
                            enhanced_tweet['geocoded_name'] = coords['display_name']
                            break
                    else:
                        enhanced_tweet['coordinates'] = {
                            'lat': coords['lat'],
                            'lon': coords['lon'],
                            'type': 'text_extraction'
                        }
                        enhanced_tweet['extracted_location'] = location
                        enhanced_tweet['geocoded_name'] = coords['display_name']
                        break

            enhanced_tweets.append(enhanced_tweet)

            # Progress indicator
            if (i + 1) % 10 == 0:
                print(f"Processed {i + 1}/{len(tweets)} tweets")

        # Count tweets with coordinates
        geolocated_count = sum(1 for t in enhanced_tweets if t.get('coordinates'))
        print(f"Successfully geolocated {geolocated_count}/{len(tweets)} tweets")

        return enhanced_tweets

    def filter_by_bounds(self, tweets: List[Dict[str, Any]], bounds: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Filter tweets to only include those within geographic bounds

        Args:
            tweets: List of tweet dictionaries
            bounds: Geographic bounds dictionary

        Returns:
            Filtered list of tweets
        """
        filtered = []
        for tweet in tweets:
            if tweet.get('coordinates'):
                coords = tweet['coordinates']
                if (bounds['min_lat'] <= coords['lat'] <= bounds['max_lat'] and
                    bounds['min_lon'] <= coords['lon'] <= bounds['max_lon']):
                    filtered.append(tweet)

        return filtered
