# Twitter Conflict Map Generator

A Python tool that collects tweets about geopolitical conflicts and visualizes them on interactive maps using geolocation data. The tool supports four major conflict zones with pre-configured settings.

## Features

- **Twitter Data Collection**: Automatically collects tweets using Twitter API v2
- **Geolocation Extraction**: Extracts location data from tweets using multiple methods:
  - Twitter's native geotag data
  - Location mentions in tweet text
  - Natural language processing to identify place names
  - Geocoding using OpenStreetMap's Nominatim
- **Interactive Maps**: Creates beautiful, interactive maps using Folium with:
  - Clustered markers for better visualization
  - Heatmaps showing tweet density
  - Detailed popups with tweet information and engagement metrics
  - Multiple map layers (OpenStreetMap, Light, Dark)
- **Pre-configured Regions**: Four ready-to-use configurations:
  - 🇺🇦 **Ukraine-Russia** conflict
  - 🇮🇱 **Israel-Iran** axis tensions
  - 🇹🇼 **China-Taiwan** relations
  - 🇻🇪 **US-Venezuela** relations

## Project Structure

```
Twitter-map/
├── configs/                    # Configuration files for each region
│   ├── ukraine_russia.json
│   ├── israel_iran.json
│   ├── china_taiwan.json
│   └── us_venezuela.json
├── data/                       # Collected tweet data (created on first run)
├── maps/                       # Generated HTML maps (created on first run)
├── index.html                 # Web dashboard interface
├── serve.py                   # Simple web server to view dashboard
├── twitter_collector.py        # Twitter API data collection module
├── geolocation.py             # Geolocation extraction and geocoding
├── map_visualizer.py          # Map creation and visualization
├── main.py                    # Main script to run everything
├── setup.sh                   # Quick setup script
├── run_all.sh                 # Generate all maps at once
├── requirements.txt           # Python dependencies
└── .env                       # API credentials (you need to create this)
```

## Installation

### Prerequisites

- Python 3.8 or higher
- Twitter API v2 access (Bearer Token required)

### Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Twitter-map
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Twitter API credentials**

   Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your Twitter API credentials:
   ```
   TWITTER_BEARER_TOKEN=your_bearer_token_here
   TWITTER_API_KEY=your_api_key_here
   TWITTER_API_SECRET=your_api_secret_here
   TWITTER_ACCESS_TOKEN=your_access_token_here
   TWITTER_ACCESS_SECRET=your_access_secret_here
   ```

   **How to get Twitter API credentials:**
   - Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
   - Create a new project and app
   - Generate your Bearer Token
   - Copy the credentials to your `.env` file

## Usage

### 🌐 Web Interface (Easiest!)

The quickest way to get started is using the web dashboard:

```bash
# Start the web server
python serve.py
```

This will:
1. Start a local web server at `http://localhost:8000`
2. Automatically open the dashboard in your browser
3. Provide a beautiful interface to:
   - View all available regions
   - Generate maps with one click
   - View maps directly in the browser
   - Access documentation

**To generate maps from the web interface:**
1. Click "Copy Command" for any region
2. Run the command in your terminal
3. Refresh the web page
4. Click "View Map" to see your generated map!

### 💻 Command Line Usage

Generate a map for any of the four regions:

```bash
# Ukraine-Russia conflict map
python main.py ukraine_russia

# Israel-Iran axis map
python main.py israel_iran

# China-Taiwan map
python main.py china_taiwan

# US-Venezuela map
python main.py us_venezuela
```

### Advanced Options

```bash
# Collect more tweets (up to 100 per run due to API limits)
python main.py ukraine_russia --max-tweets 100

# Create map without heatmap layer
python main.py israel_iran --no-heatmap

# Use existing data file instead of collecting new tweets
python main.py china_taiwan --skip-collection

# Use a specific data file
python main.py us_venezuela --data-file data/us_venezuela_100_tweets.json
```

### Command Line Arguments

- `region`: Required. Choose from: `ukraine_russia`, `israel_iran`, `china_taiwan`, `us_venezuela`
- `--max-tweets`: Number of tweets to collect (default: 100, max: 100)
- `--no-heatmap`: Disable the heatmap layer
- `--skip-collection`: Use most recent data file instead of collecting new tweets
- `--data-file`: Specify a specific data file to use

### Example Workflow

```bash
# 1. Collect tweets and generate map for Ukraine-Russia
python main.py ukraine_russia --max-tweets 100

# 2. Generated files:
#    - data/ukraine_russia_100_tweets.json (raw tweet data)
#    - maps/ukraine_russia_map.html (interactive map)

# 3. Open the map in your browser
# On Linux/Mac:
open maps/ukraine_russia_map.html
# On Windows:
start maps/ukraine_russia_map.html
```

## 🌐 Deploy as a Website (GitHub Pages)

You can host your generated maps as a public website using GitHub Pages!

### Quick Deploy

```bash
# 1. Generate your maps
python main.py ukraine_russia
python main.py israel_iran
python main.py china_taiwan
python main.py us_venezuela

# 2. Copy maps to docs folder
./deploy_to_pages.sh

# 3. Push to GitHub
git add docs/
git commit -m "Deploy maps to GitHub Pages"
git push origin main
```

### Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** → **Pages**
3. Under **Source**:
   - Branch: `main`
   - Folder: `/docs`
4. Click **Save**

Your website will be live at: `https://yourusername.github.io/Twitter-map/`

### Features of the Website

- ✅ Beautiful dashboard interface
- ✅ View all 4 conflict region maps
- ✅ Interactive map viewer
- ✅ No server required (static HTML)
- ✅ Free hosting on GitHub

**Note:** The website displays pre-generated maps. To update with fresh data, regenerate maps locally and re-deploy.

## How It Works

### 1. Tweet Collection
The tool searches Twitter for recent tweets (last 7 days) matching configured keywords and hashtags for each region. It collects:
- Tweet text and metadata
- Author information
- Engagement metrics (likes, retweets, replies)
- Native geolocation data (if available)

### 2. Geolocation Processing
Multiple methods are used to determine tweet locations:
- **Native Geotags**: If the tweet has location data attached
- **Text Analysis**: Extracts location mentions from tweet text
- **Keyword Matching**: Identifies configured location keywords
- **Geocoding**: Converts location names to coordinates using Nominatim

### 3. Map Visualization
Interactive maps are created with:
- **Marker Clustering**: Groups nearby tweets for better visualization
- **Color-coded Markers**:
  - 🔴 Red: High engagement (>1000 interactions)
  - 🟠 Orange: Medium engagement (100-1000)
  - 🔵 Blue: Low engagement (10-100)
  - 🟢 Green: Minimal engagement (<10)
- **Heatmap Layer**: Shows density of tweet activity
- **Interactive Popups**: Click markers to see full tweet details

## Configuration

Each region has a JSON configuration file in `configs/` with:

```json
{
  "name": "Region Name",
  "description": "Description",
  "keywords": ["keyword1", "keyword2"],
  "hashtags": ["#hashtag1", "#hashtag2"],
  "geographic_bounds": {
    "min_lat": 0.0,
    "max_lat": 0.0,
    "min_lon": 0.0,
    "max_lon": 0.0
  },
  "center_coords": {
    "lat": 0.0,
    "lon": 0.0
  },
  "zoom_level": 6
}
```

### Customization

You can create your own region configuration by:
1. Copying an existing config file
2. Modifying keywords, hashtags, and geographic bounds
3. Running with your custom config name

## API Limits and Rate Limiting

- Twitter API v2 Free tier: 500,000 tweets/month
- Search recent tweets: 100 results per request
- Rate limits are automatically handled by the tool
- Geocoding has built-in delays to respect OpenStreetMap's usage policy

## Output Files

### Data Files (`data/`)
JSON files containing collected tweet data:
```json
[
  {
    "id": "tweet_id",
    "text": "tweet text",
    "created_at": "timestamp",
    "author_username": "username",
    "likes": 123,
    "retweets": 45,
    "replies": 6,
    "coordinates": {
      "lat": 50.45,
      "lon": 30.52,
      "type": "text_extraction"
    },
    "extracted_location": "Kyiv"
  }
]
```

### Map Files (`maps/`)
HTML files with interactive Folium maps that can be opened in any web browser.

## Troubleshooting

### No tweets collected
- Check your Twitter API credentials in `.env`
- Verify your API access level supports search functionality
- Try different keywords or time periods
- Check if you've hit rate limits

### Low geolocation success rate
- Twitter users often don't enable location services
- Text-based extraction depends on users mentioning locations
- Some regions may have less geotagged content
- Typical geolocation rates: 10-30% of tweets

### Geocoding errors
- Nominatim (OpenStreetMap) has usage limits
- The tool includes delays to respect these limits
- Some location names may be ambiguous
- Geographic bounds help constrain search area

## Privacy and Ethics

This tool is designed for research and analysis purposes. Please:
- Respect Twitter's Terms of Service
- Respect user privacy and data protection laws
- Use collected data responsibly
- Don't use for surveillance or harassment
- Be aware of the sensitivity of conflict-related data

## Contributing

Contributions are welcome! Areas for improvement:
- Additional region configurations
- Enhanced geolocation algorithms
- Better visualization options
- Support for historical data
- Sentiment analysis integration

## License

This project is provided as-is for educational and research purposes.

## Dependencies

- `tweepy`: Twitter API client
- `folium`: Interactive map generation
- `geopy`: Geocoding service
- `pandas`: Data manipulation
- `python-dotenv`: Environment variable management

## Support

For issues, questions, or contributions, please open an issue on GitHub.

---

**Note**: This tool requires Twitter API access. Free tier access has limitations. For production use or large-scale data collection, consider Twitter's paid API tiers.
