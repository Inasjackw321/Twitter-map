"""
Map Visualization Module
Creates interactive maps with geolocated tweets
"""

import folium
from folium.plugins import MarkerCluster, HeatMap
from typing import List, Dict, Any
import os
from datetime import datetime


class MapVisualizer:
    """Creates interactive maps using Folium"""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize map visualizer

        Args:
            config: Configuration dictionary with map settings
        """
        self.config = config
        self.center_coords = [
            config['center_coords']['lat'],
            config['center_coords']['lon']
        ]
        self.zoom_level = config.get('zoom_level', 6)

    def create_base_map(self) -> folium.Map:
        """Create base map centered on region"""
        base_map = folium.Map(
            location=self.center_coords,
            zoom_start=self.zoom_level,
            tiles='OpenStreetMap'
        )

        # Add alternative tile layers
        folium.TileLayer('CartoDB positron', name='Light Map').add_to(base_map)
        folium.TileLayer('CartoDB dark_matter', name='Dark Map').add_to(base_map)

        return base_map

    def add_tweet_markers(self, map_obj: folium.Map, tweets: List[Dict[str, Any]], use_clustering: bool = True):
        """
        Add tweet markers to map

        Args:
            map_obj: Folium map object
            tweets: List of geolocated tweets
            use_clustering: Whether to use marker clustering
        """
        # Filter tweets with coordinates
        geolocated_tweets = [t for t in tweets if t.get('coordinates')]

        if not geolocated_tweets:
            print("No geolocated tweets to display")
            return

        # Create marker cluster if requested
        if use_clustering:
            marker_cluster = MarkerCluster(name='Tweet Locations').add_to(map_obj)
            marker_group = marker_cluster
        else:
            marker_group = folium.FeatureGroup(name='Tweet Locations').add_to(map_obj)

        # Add markers
        for tweet in geolocated_tweets:
            coords = tweet['coordinates']
            lat, lon = coords['lat'], coords['lon']

            # Create popup content
            popup_html = self._create_popup_html(tweet)

            # Determine marker color based on engagement
            color = self._get_marker_color(tweet)

            # Create marker
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"@{tweet['author_username']}: {tweet['text'][:50]}...",
                icon=folium.Icon(color=color, icon='info-sign')
            ).add_to(marker_group)

        print(f"Added {len(geolocated_tweets)} markers to map")

    def add_heatmap(self, map_obj: folium.Map, tweets: List[Dict[str, Any]]):
        """
        Add heatmap layer showing tweet density

        Args:
            map_obj: Folium map object
            tweets: List of geolocated tweets
        """
        # Filter tweets with coordinates
        geolocated_tweets = [t for t in tweets if t.get('coordinates')]

        if not geolocated_tweets:
            return

        # Create heatmap data
        heat_data = [
            [tweet['coordinates']['lat'], tweet['coordinates']['lon']]
            for tweet in geolocated_tweets
        ]

        # Add heatmap layer
        HeatMap(
            heat_data,
            name='Tweet Density Heatmap',
            min_opacity=0.3,
            radius=15,
            blur=25,
            gradient={0.4: 'blue', 0.65: 'lime', 0.8: 'yellow', 1.0: 'red'}
        ).add_to(map_obj)

        print(f"Added heatmap with {len(heat_data)} points")

    def _create_popup_html(self, tweet: Dict[str, Any]) -> str:
        """Create HTML content for marker popup"""
        html = f"""
        <div style="width: 280px;">
            <h4 style="margin-bottom: 5px;">@{tweet['author_username']}</h4>
            <p style="margin: 5px 0;"><strong>Tweet:</strong><br>{tweet['text'][:200]}</p>
            <hr style="margin: 5px 0;">
            <p style="margin: 5px 0; font-size: 0.9em;">
                <strong>❤️</strong> {tweet['likes']} &nbsp;
                <strong>🔄</strong> {tweet['retweets']} &nbsp;
                <strong>💬</strong> {tweet['replies']}
            </p>
            <p style="margin: 5px 0; font-size: 0.85em; color: #666;">
                {tweet['created_at'][:10]}
            </p>
        """

        if tweet.get('extracted_location'):
            html += f"""
            <p style="margin: 5px 0; font-size: 0.85em; color: #0066cc;">
                📍 {tweet['extracted_location']}
            </p>
            """

        if tweet.get('place'):
            html += f"""
            <p style="margin: 5px 0; font-size: 0.85em; color: #0066cc;">
                📍 {tweet['place']['name']}
            </p>
            """

        html += "</div>"
        return html

    def _get_marker_color(self, tweet: Dict[str, Any]) -> str:
        """Determine marker color based on engagement metrics"""
        total_engagement = tweet['likes'] + tweet['retweets'] + tweet['replies']

        if total_engagement > 1000:
            return 'red'
        elif total_engagement > 100:
            return 'orange'
        elif total_engagement > 10:
            return 'blue'
        else:
            return 'green'

    def create_map(self, tweets: List[Dict[str, Any]], output_filename: str, include_heatmap: bool = True):
        """
        Create complete interactive map

        Args:
            tweets: List of tweets to visualize
            output_filename: Output HTML filename
            include_heatmap: Whether to include heatmap layer
        """
        print(f"\nCreating map for {self.config['name']}...")

        # Create base map
        map_obj = self.create_base_map()

        # Add tweet markers
        self.add_tweet_markers(map_obj, tweets, use_clustering=True)

        # Add heatmap if requested
        if include_heatmap:
            self.add_heatmap(map_obj, tweets)

        # Add layer control
        folium.LayerControl().add_to(map_obj)

        # Add title
        title_html = f'''
        <div style="position: fixed;
                    top: 10px; left: 50px; width: 400px; height: 60px;
                    background-color: white; border:2px solid grey; z-index:9999;
                    font-size:16px; padding: 10px; opacity: 0.9;">
            <h3 style="margin:0;">{self.config['name']}</h3>
            <p style="margin:5px 0; font-size:12px;">{self.config['description']}</p>
        </div>
        '''
        map_obj.get_root().html.add_child(folium.Element(title_html))

        # Add statistics
        geolocated_count = sum(1 for t in tweets if t.get('coordinates'))
        stats_html = f'''
        <div style="position: fixed;
                    bottom: 10px; left: 10px; width: 200px;
                    background-color: white; border:2px solid grey; z-index:9999;
                    font-size:12px; padding: 10px; opacity: 0.9;">
            <p style="margin:2px;"><strong>Total Tweets:</strong> {len(tweets)}</p>
            <p style="margin:2px;"><strong>Geolocated:</strong> {geolocated_count}</p>
            <p style="margin:2px;"><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        </div>
        '''
        map_obj.get_root().html.add_child(folium.Element(stats_html))

        # Save map
        os.makedirs('maps', exist_ok=True)
        filepath = os.path.join('maps', output_filename)
        map_obj.save(filepath)

        print(f"Map saved to {filepath}")
        return filepath
