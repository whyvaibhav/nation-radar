// Nation Radar - Clean Dashboard JavaScript

// Configuration
const BASE_API_URL = window.location.origin;
const VPS_API_URL = 'http://143.198.226.161:5001';

// State
let currentData = {
    tweets: [],
    leaderboard: [],
    stats: {}
};

// DOM Elements
const loadingOverlay = document.getElementById('loading-overlay');
const trendingContent = document.getElementById('trending-content');
const leaderboard = document.getElementById('leaderboard');
const activityFeed = document.getElementById('activity-feed');
const totalUsers = document.getElementById('total-users');
const avgScore = document.getElementById('avg-score');
const totalContent = document.getElementById('total-content');
const lastUpdate = document.getElementById('last-update');

// Main Functions
async function fetchData() {
    try {
        showLoading(true);
        
        // Fetch data from VPS API
        const [tweetsResponse, leaderboardResponse, statsResponse] = await Promise.all([
            fetch(`${VPS_API_URL}/api/tweets`),
            fetch(`${VPS_API_URL}/api/leaderboard`),
            fetch(`${VPS_API_URL}/api/stats`)
        ]);

        if (!tweetsResponse.ok || !leaderboardResponse.ok || !statsResponse.ok) {
            throw new Error('Failed to fetch data from VPS');
        }

        const tweets = await tweetsResponse.json();
        const leaderboardData = await leaderboardResponse.json();
        const stats = await statsResponse.json();

        // Update state
        currentData = {
            tweets: tweets.data || [],
            leaderboard: leaderboardData.data || [],
            stats: stats.statistics || {}
        };

        // Update UI
        updateDashboard();
        updateLastUpdate();
        
    } catch (error) {
        console.error('Error fetching data:', error);
        showNotification('Failed to fetch data. Please check VPS connection.', 'error');
    } finally {
        showLoading(false);
    }
}

function updateDashboard() {
    updateHeroStats();
    renderTrendingContent();
    renderLeaderboard();
    renderRecentActivity();
}

function updateHeroStats() {
    const stats = currentData.stats;
    
    totalUsers.textContent = stats.total_tweets || 0;
    avgScore.textContent = (stats.average_score || 0).toFixed(3);
    totalContent.textContent = stats.scored_tweets || 0;
}

function renderTrendingContent() {
    if (!currentData.tweets.length) {
        trendingContent.innerHTML = '<p class="no-data">No trending content available</p>';
        return;
    }

    const topTweets = currentData.tweets.slice(0, 6);
    
    trendingContent.innerHTML = topTweets.map(tweet => `
        <div class="content-card fade-in">
            <div class="card-header">
                <div class="user-info">
                    <div class="user-avatar">${getInitials(tweet.username)}</div>
                    <div>
                        <h4>@${tweet.username}</h4>
                        <span class="timestamp">${formatTime(tweet.created_at)}</span>
                    </div>
                </div>
                <div class="score-badge">${(tweet.score || 0).toFixed(3)}</div>
            </div>
            <div class="card-content">
                <p>${tweet.text}</p>
            </div>
            <div class="card-footer">
                <div class="engagement-stats">
                    <span><i class="fas fa-heart"></i> ${tweet.engagement?.likes || 0}</span>
                    <span><i class="fas fa-retweet"></i> ${tweet.engagement?.retweets || 0}</span>
                    <span><i class="fas fa-comment"></i> ${tweet.engagement?.replies || 0}</span>
                    <span><i class="fas fa-eye"></i> ${tweet.engagement?.views || 0}</span>
                </div>
                <div class="total-engagement">
                    Total: ${calculateTotalEngagement(tweet.engagement)}
                </div>
            </div>
        </div>
    `).join('');
}

function renderLeaderboard() {
    if (!currentData.leaderboard.length) {
        leaderboard.innerHTML = '<p class="no-data">No leaderboard data available</p>';
        return;
    }

    const topUsers = currentData.leaderboard.slice(0, 10);
    
    leaderboard.innerHTML = topUsers.map((tweet, index) => `
        <div class="leaderboard-item fade-in">
            <div class="leaderboard-rank ${index < 3 ? 'top-3' : ''}">${index + 1}</div>
            <div class="leaderboard-user">
                <div class="user-avatar">${getInitials(tweet.username)}</div>
                <div class="user-info">
                    <h4>@${tweet.username}</h4>
                    <p>${tweet.text.substring(0, 100)}${tweet.text.length > 100 ? '...' : ''}</p>
                </div>
            </div>
            <div class="leaderboard-score">${(tweet.score || 0).toFixed(3)}</div>
        </div>
    `).join('');
}

function renderRecentActivity() {
    if (!currentData.tweets.length) {
        activityFeed.innerHTML = '<p class="no-data">No recent activity available</p>';
        return;
    }

    const recentTweets = currentData.tweets.slice(0, 8);
    
    activityFeed.innerHTML = recentTweets.map(tweet => `
        <div class="activity-item fade-in">
            <div class="activity-header">
                <div class="activity-avatar">${getInitials(tweet.username)}</div>
                <div class="activity-meta">
                    <h4>@${tweet.username}</h4>
                    <p>${formatTime(tweet.created_at)}</p>
                </div>
                <div class="activity-score">${(tweet.score || 0).toFixed(3)}</div>
            </div>
            <div class="activity-content">
                ${tweet.text}
            </div>
        </div>
    `).join('');
}

function updateLastUpdate() {
    const now = new Date();
    lastUpdate.textContent = now.toLocaleString();
}

// Utility Functions
function getInitials(username) {
    return username
        .split('_')
        .map(word => word.charAt(0).toUpperCase())
        .join('')
        .substring(0, 2);
}

function formatTime(timestamp) {
    if (!timestamp) return 'Unknown';
    
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    
    return date.toLocaleDateString();
}

function calculateTotalEngagement(engagement) {
    if (!engagement) return 0;
    
    return (
        (engagement.likes || 0) +
        (engagement.retweets || 0) +
        (engagement.replies || 0) +
        (engagement.views || 0) +
        (engagement.bookmarks || 0) +
        (engagement.quote_tweets || 0)
    );
}

function showLoading(show) {
    loadingOverlay.style.display = show ? 'flex' : 'none';
}

function showNotification(message, type = 'info') {
    // Simple notification - you can enhance this later
    console.log(`${type.toUpperCase()}: ${message}`);
}

// Event Listeners
function setupEventListeners() {
    // Auto-refresh every 30 seconds
    setInterval(fetchData, 30000);
    
    // Initial load
    fetchData();
}

// Initialize Dashboard
function initDashboard() {
    setupEventListeners();
}

// Start the dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', initDashboard);

// Add some CSS for no-data states
const style = document.createElement('style');
style.textContent = `
    .no-data {
        text-align: center;
        color: var(--text-muted);
        padding: 2rem;
        font-style: italic;
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
`;
document.head.appendChild(style);