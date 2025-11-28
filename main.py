#!/usr/bin/env python3
"""
Twitter Conflict Map Generator
Main script to collect tweets and generate geolocation maps for various conflicts
"""

import argparse
import json
import sys
import os
from twitter_collector import TwitterCollector
from geolocation import GeolocatorService
from map_visualizer import MapVisualizer


def load_config(config_name: str) -> dict:
    """Load configuration file"""
    config_path = os.path.join('configs', f'{config_name}.json')

    if not os.path.exists(config_path):
        print(f"Error: Configuration file not found: {config_path}")
        print("\nAvailable configurations:")
        print("  - ukraine_russia")
        print("  - israel_iran")
        print("  - china_taiwan")
        print("  - us_venezuela")
        sys.exit(1)

    with open(config_path, 'r') as f:
        return json.load(f)


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description='Twitter Conflict Map Generator - Collect and map geolocated tweets',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate Ukraine-Russia conflict map
  python main.py ukraine_russia

  # Generate Israel-Iran map with 200 tweets
  python main.py israel_iran --max-tweets 200

  # Generate China-Taiwan map without heatmap
  python main.py china_taiwan --no-heatmap

Available regions:
  ukraine_russia  - Ukraine-Russia conflict
  israel_iran     - Israel-Iran axis tensions
  china_taiwan    - China-Taiwan relations
  us_venezuela    - US-Venezuela relations
        """
    )

    parser.add_argument(
        'region',
        choices=['ukraine_russia', 'israel_iran', 'china_taiwan', 'us_venezuela'],
        help='Region/conflict to map'
    )
    parser.add_argument(
        '--max-tweets',
        type=int,
        default=100,
        help='Maximum number of tweets to collect (default: 100, max: 100 due to API limits)'
    )
    parser.add_argument(
        '--no-heatmap',
        action='store_true',
        help='Disable heatmap layer on the map'
    )
    parser.add_argument(
        '--skip-collection',
        action='store_true',
        help='Skip tweet collection and use existing data file'
    )
    parser.add_argument(
        '--data-file',
        type=str,
        help='Use specific data file instead of collecting new tweets'
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Twitter Conflict Map Generator")
    print("=" * 60)

    # Load configuration
    print(f"\nLoading configuration for: {args.region}")
    config = load_config(args.region)
    print(f"Region: {config['name']}")
    print(f"Description: {config['description']}")

    # Initialize services
    tweets_data = []

    if args.data_file:
        # Load from specific file
        print(f"\nLoading tweets from: {args.data_file}")
        with open(args.data_file, 'r') as f:
            tweets_data = json.load(f)
        print(f"Loaded {len(tweets_data)} tweets")

    elif not args.skip_collection:
        # Collect tweets
        print("\n" + "=" * 60)
        print("Step 1: Collecting Tweets")
        print("=" * 60)

        try:
            collector = TwitterCollector()
            tweets_data = collector.collect_tweets(config, max_results=args.max_tweets)

            if not tweets_data:
                print("\nNo tweets collected. This could be due to:")
                print("  - No recent tweets matching the criteria")
                print("  - Twitter API credentials not configured")
                print("  - API rate limits reached")
                print("\nPlease check your .env file and API access level")
                sys.exit(1)

            # Save collected tweets
            data_filename = f"{args.region}_{len(tweets_data)}_tweets.json"
            collector.save_tweets(tweets_data, data_filename)

        except Exception as e:
            print(f"\nError collecting tweets: {e}")
            print("\nMake sure you have:")
            print("  1. Created a .env file with your Twitter API credentials")
            print("  2. Installed all requirements: pip install -r requirements.txt")
            sys.exit(1)
    else:
        # Try to load most recent data file
        data_dir = 'data'
        if os.path.exists(data_dir):
            files = [f for f in os.listdir(data_dir) if f.startswith(args.region) and f.endswith('.json')]
            if files:
                latest_file = sorted(files)[-1]
                filepath = os.path.join(data_dir, latest_file)
                print(f"\nLoading tweets from: {filepath}")
                with open(filepath, 'r') as f:
                    tweets_data = json.load(f)
                print(f"Loaded {len(tweets_data)} tweets")
            else:
                print(f"\nNo existing data file found for {args.region}")
                sys.exit(1)
        else:
            print("\nNo data directory found. Cannot skip collection.")
            sys.exit(1)

    # Process geolocation
    print("\n" + "=" * 60)
    print("Step 2: Processing Geolocation")
    print("=" * 60)

    geolocator = GeolocatorService()
    enhanced_tweets = geolocator.process_tweets_geolocation(tweets_data, config)

    # Create map
    print("\n" + "=" * 60)
    print("Step 3: Creating Map Visualization")
    print("=" * 60)

    visualizer = MapVisualizer(config)
    output_filename = f"{args.region}_map.html"
    map_path = visualizer.create_map(
        enhanced_tweets,
        output_filename,
        include_heatmap=not args.no_heatmap
    )

    # Final summary
    print("\n" + "=" * 60)
    print("COMPLETE!")
    print("=" * 60)
    geolocated_count = sum(1 for t in enhanced_tweets if t.get('coordinates'))
    print(f"\nTotal tweets collected: {len(enhanced_tweets)}")
    print(f"Successfully geolocated: {geolocated_count} ({geolocated_count/len(enhanced_tweets)*100:.1f}%)")
    print(f"\nMap saved to: {map_path}")
    print(f"\nOpen the map in your browser to view the results!")


if __name__ == '__main__':
    main()
