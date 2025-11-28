// Twitter Conflict Map Generator - Client-Side Application
// Generates realistic demo data and creates interactive maps

// Configuration for each region
const REGIONS = {
    ukraine_russia: {
        name: "Ukraine-Russia Conflict",
        description: "Tracking Ukraine-Russia conflict related activity",
        center: [48.379433, 31.16558],
        zoom: 6,
        bounds: [[44.0, 22.0], [52.5, 40.5]],
        keywords: ["Ukraine", "Russia", "Kyiv", "Kiev", "Donbas", "Crimea", "Zelensky", "Putin", "Wagner", "Bakhmut"],
        sampleTweets: [
            "Breaking news from #Kyiv - humanitarian aid arriving",
            "Situation update in eastern #Ukraine",
            "International response to ongoing conflict in #Donbas",
            "Diplomatic efforts continue in #Kiev",
            "Civilians evacuated from #Bakhmut region",
            "NATO support for #Ukraine discussed",
            "Updates from #Crimea peninsula",
            "Russian forces activity near border",
            "Ukrainian defense forces holding positions",
            "Peace talks proposed for conflict resolution"
        ],
        cities: [
            {name: "Kyiv", coords: [50.4501, 30.5234]},
            {name: "Kharkiv", coords: [49.9935, 36.2304]},
            {name: "Odesa", coords: [46.4825, 30.7233]},
            {name: "Dnipro", coords: [48.4647, 35.0462]},
            {name: "Donetsk", coords: [48.0159, 37.8029]},
            {name: "Lviv", coords: [49.8397, 24.0297]},
            {name: "Mariupol", coords: [47.0971, 37.5432]},
            {name: "Zaporizhzhia", coords: [47.8388, 35.1396]}
        ]
    },
    israel_iran: {
        name: "Israel-Iran Axis",
        description: "Tracking Israel-Iran axis tensions",
        center: [31.0461, 34.8516],
        zoom: 5,
        bounds: [[15.0, 34.0], [42.0, 63.0]],
        keywords: ["Israel", "Iran", "Gaza", "Hamas", "Hezbollah", "Lebanon", "Tehran", "Jerusalem", "Tel Aviv", "IDF"],
        sampleTweets: [
            "Situation report from #Gaza strip",
            "#Israel defense updates from the region",
            "International community responds to Middle East tensions",
            "Humanitarian situation in #Gaza deteriorating",
            "#Lebanon border situation monitored",
            "Diplomatic efforts in #Jerusalem ongoing",
            "Regional tensions escalate near #Tehran",
            "#IDF operations in the area",
            "Ceasefire negotiations continue",
            "Aid convoy heading to affected areas"
        ],
        cities: [
            {name: "Jerusalem", coords: [31.7683, 35.2137]},
            {name: "Tel Aviv", coords: [32.0853, 34.7818]},
            {name: "Gaza City", coords: [31.5, 34.467]},
            {name: "Beirut", coords: [33.8886, 35.4955]},
            {name: "Damascus", coords: [33.5138, 36.2765]},
            {name: "Tehran", coords: [35.6892, 51.3890]},
            {name: "Haifa", coords: [32.7940, 34.9896]},
            {name: "Amman", coords: [31.9454, 35.9284]}
        ]
    },
    china_taiwan: {
        name: "China-Taiwan",
        description: "Tracking China-Taiwan relations",
        center: [23.6978, 120.9605],
        zoom: 7,
        bounds: [[21.5, 118.0], [26.0, 122.5]],
        keywords: ["Taiwan", "China", "PRC", "ROC", "Taipei", "Beijing", "Taiwan Strait", "TSMC"],
        sampleTweets: [
            "#Taiwan Strait tensions monitored closely",
            "Diplomatic statement from #Taipei released",
            "#China military exercises in the region",
            "International reaction to cross-strait relations",
            "Economic ties between #Taiwan and mainland discussed",
            "Defense preparedness in #Taipei increased",
            "US support for #Taiwan reaffirmed",
            "Trade negotiations continue despite tensions",
            "Regional stability concerns raised",
            "Technology sector impact from #Taiwan situation"
        ],
        cities: [
            {name: "Taipei", coords: [25.0330, 121.5654]},
            {name: "Kaohsiung", coords: [22.6273, 120.3014]},
            {name: "Taichung", coords: [24.1477, 120.6736]},
            {name: "Tainan", coords: [22.9998, 120.2269]},
            {name: "Hsinchu", coords: [24.8138, 120.9675]},
            {name: "Keelung", coords: [25.1276, 121.7392]}
        ]
    },
    us_venezuela: {
        name: "US-Venezuela",
        description: "Tracking US-Venezuela relations",
        center: [6.4238, -66.5897],
        zoom: 6,
        bounds: [[-5.0, -73.5], [12.5, -59.5]],
        keywords: ["Venezuela", "USA", "Maduro", "Caracas", "sanctions", "migration", "border"],
        sampleTweets: [
            "Economic sanctions impact on #Venezuela discussed",
            "Migration crisis from #Venezuela continues",
            "US policy towards #Caracas under review",
            "Humanitarian situation in #Venezuela worsening",
            "Regional response to #Venezuela crisis",
            "Oil production in #Venezuela declining",
            "International aid efforts for #Venezuela",
            "Border situation with Colombia monitored",
            "Political tensions in #Caracas escalate",
            "Diplomatic negotiations ongoing"
        ],
        cities: [
            {name: "Caracas", coords: [10.4806, -66.9036]},
            {name: "Maracaibo", coords: [10.6666, -71.6122]},
            {name: "Valencia", coords: [10.1621, -68.0077]},
            {name: "Barquisimeto", coords: [10.0647, -69.3570]},
            {name: "Maracay", coords: [10.2469, -67.5958]},
            {name: "Ciudad Guayana", coords: [8.3792, -62.6182]}
        ]
    }
};

// Generate realistic demo data
function generateDemoData(region, count = 50) {
    const config = REGIONS[region];
    const tweets = [];
    const now = new Date();

    for (let i = 0; i < count; i++) {
        // Random city
        const city = config.cities[Math.floor(Math.random() * config.cities.length)];

        // Add some randomness to coordinates
        const lat = city.coords[0] + (Math.random() - 0.5) * 0.3;
        const lon = city.coords[1] + (Math.random() - 0.5) * 0.3;

        // Check if within bounds
        if (lat < config.bounds[0][0] || lat > config.bounds[1][0] ||
            lon < config.bounds[0][1] || lon > config.bounds[1][1]) {
            continue;
        }

        // Random tweet text
        const tweetText = config.sampleTweets[Math.floor(Math.random() * config.sampleTweets.length)];

        // Random engagement metrics
        const likes = Math.floor(Math.random() * 5000);
        const retweets = Math.floor(Math.random() * 1000);
        const replies = Math.floor(Math.random() * 500);

        // Random timestamp within last 7 days
        const daysAgo = Math.floor(Math.random() * 7);
        const timestamp = new Date(now.getTime() - daysAgo * 24 * 60 * 60 * 1000);

        tweets.push({
            id: `demo_${i}`,
            text: tweetText,
            author: `user${Math.floor(Math.random() * 1000)}`,
            coordinates: {lat, lon},
            location: city.name,
            likes,
            retweets,
            replies,
            timestamp: timestamp.toISOString(),
            engagement: likes + retweets + replies
        });
    }

    return tweets;
}

// Create map with Leaflet
function createMap(region, tweets) {
    const config = REGIONS[region];

    // Create map
    const map = L.map('map').setView(config.center, config.zoom);

    // Add tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(map);

    // Add markers
    tweets.forEach(tweet => {
        const color = getMarkerColor(tweet.engagement);
        const icon = L.divIcon({
            className: 'custom-marker',
            html: `<div style="background-color: ${color}; width: 12px; height: 12px; border-radius: 50%; border: 2px solid white;"></div>`,
            iconSize: [12, 12]
        });

        const marker = L.marker([tweet.coordinates.lat, tweet.coordinates.lon], {icon})
            .addTo(map);

        // Create popup
        const popupContent = `
            <div style="min-width: 200px;">
                <h4 style="margin: 0 0 10px 0;">@${tweet.author}</h4>
                <p style="margin: 5px 0;">${tweet.text}</p>
                <hr style="margin: 10px 0;">
                <p style="margin: 5px 0; font-size: 0.9em;">
                    <strong>❤️</strong> ${tweet.likes} &nbsp;
                    <strong>🔄</strong> ${tweet.retweets} &nbsp;
                    <strong>💬</strong> ${tweet.replies}
                </p>
                <p style="margin: 5px 0; font-size: 0.85em; color: #666;">
                    📍 ${tweet.location}
                </p>
                <p style="margin: 5px 0; font-size: 0.85em; color: #999;">
                    ${new Date(tweet.timestamp).toLocaleDateString()}
                </p>
            </div>
        `;

        marker.bindPopup(popupContent);
    });

    // Add heatmap layer
    const heatData = tweets.map(t => [t.coordinates.lat, t.coordinates.lon, t.engagement / 1000]);
    L.heatLayer(heatData, {
        radius: 25,
        blur: 35,
        maxZoom: 10,
        gradient: {0.4: 'blue', 0.65: 'lime', 0.8: 'yellow', 1: 'red'}
    }).addTo(map);

    return map;
}

// Get marker color based on engagement
function getMarkerColor(engagement) {
    if (engagement > 1000) return '#dc2626';  // red
    if (engagement > 100) return '#f97316';   // orange
    if (engagement > 10) return '#3b82f6';    // blue
    return '#10b981';                         // green
}

// Update stats display
function updateStats(region, tweets) {
    const stats = document.getElementById('stats');
    const config = REGIONS[region];

    const totalEngagement = tweets.reduce((sum, t) => sum + t.engagement, 0);
    const avgEngagement = Math.floor(totalEngagement / tweets.length);

    stats.innerHTML = `
        <div class="stat-card">
            <h3>${config.name}</h3>
            <p>${config.description}</p>
        </div>
        <div class="stat-card">
            <div class="stat-number">${tweets.length}</div>
            <div class="stat-label">Total Posts</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">${tweets.length}</div>
            <div class="stat-label">Geolocated</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">${avgEngagement.toLocaleString()}</div>
            <div class="stat-label">Avg Engagement</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">${new Date().toLocaleDateString()}</div>
            <div class="stat-label">Generated</div>
        </div>
    `;
}

// Initialize app
let currentMap = null;
let currentRegion = 'ukraine_russia';

function loadRegion(region) {
    currentRegion = region;

    // Show loading
    document.getElementById('loading').style.display = 'flex';

    // Update active button
    document.querySelectorAll('.region-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-region="${region}"]`).classList.add('active');

    // Simulate loading delay for realism
    setTimeout(() => {
        // Generate demo data
        const tweets = generateDemoData(region, 50);

        // Remove old map
        if (currentMap) {
            currentMap.remove();
        }

        // Create new map
        currentMap = createMap(region, tweets);

        // Update stats
        updateStats(region, tweets);

        // Hide loading
        document.getElementById('loading').style.display = 'none';
    }, 500);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    loadRegion('ukraine_russia');
});
