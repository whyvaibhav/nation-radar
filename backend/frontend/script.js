// Nation Radar - Enhanced Frontend JavaScript
class NationRadar {
    constructor() {
        this.data = [];
        this.leaderboard = [];
        this.isLoading = false;
        this.init();
    }

    async init() {
        await this.loadData();
        await this.loadLeaderboard();
        this.setupEventListeners();
        
        // Auto-refresh every 5 minutes
        setInterval(() => this.loadData(), 5 * 60 * 1000);
    }

    setupEventListeners() {
        // Add any additional event listeners here
        document.addEventListener('DOMContentLoaded', () => {
            this.updateLastUpdateTime();
        });
    }

    async loadData() {
        if (this.isLoading) return;
        this.isLoading = true;

        try {
            const response = await fetch('/api/crestal-data');
            const result = await response.json();

            if (result.success) {
                this.data = result.data || [];
                this.updateStats(result.stats);
                this.displayTweets(this.data);
            } else {
                console.error('Failed to load data:', result.error);
                this.showError('Failed to load tweet data');
            }
        } catch (error) {
            console.error('API error:', error);
            this.showError('Connection error - using cached data');
        } finally {
            this.isLoading = false;
        }
    }

    async loadLeaderboard() {
        try {
            const response = await fetch('/api/leaderboard?limit=20');
            const result = await response.json();

            if (result.success) {
                this.leaderboard = result.leaderboard || [];
                this.displayLeaderboard(this.leaderboard);
            } else {
                console.error('Failed to load leaderboard:', result.error);
            }
        } catch (error) {
            console.error('Leaderboard error:', error);
        }
    }

    updateStats(stats) {
        const elements = {
            'total-tweets': stats?.total_tweets || this.data.length,
            'avg-score': (stats?.avg_score || this.calculateAverageScore()).toFixed(2),
            'active-contributors': stats?.unique_users || this.getUniqueContributors(),
        };

        Object.entries(elements).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) {
                this.animateNumber(element, value);
            }
        });

        this.updateLastUpdateTime();
    }

    calculateAverageScore() {
        if (this.data.length === 0) return 0;
        const sum = this.data.reduce((acc, tweet) => acc + (parseFloat(tweet.score) || 0), 0);
        return sum / this.data.length;
    }

    getUniqueContributors() {
        const users = new Set(this.data.map(tweet => tweet.username));
        return users.size;
    }

    animateNumber(element, targetValue) {
        const currentValue = parseFloat(element.textContent) || 0;
        const increment = (targetValue - currentValue) / 20;
        let current = currentValue;
        
        const animation = setInterval(() => {
            current += increment;
            if ((increment > 0 && current >= targetValue) || (increment < 0 && current <= targetValue)) {
                current = targetValue;
                clearInterval(animation);
            }
            
            if (typeof targetValue === 'string') {
                element.textContent = targetValue;
            } else {
                element.textContent = Math.round(current * 100) / 100;
            }
        }, 50);
    }

    updateLastUpdateTime() {
        const element = document.getElementById('last-update');
        if (element) {
            const now = new Date();
            element.textContent = now.toLocaleTimeString();
        }
    }

    displayLeaderboard(leaderboard) {
        const tbody = document.getElementById('leaderboard-body');
        if (!tbody) return;

        if (leaderboard.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="6" style="text-align: center; color: var(--text-dim);">
                        No data available yet. Pipeline will populate this soon.
                    </td>
                </tr>
            `;
            return;
        }

        tbody.innerHTML = leaderboard.map((user, index) => `
            <tr>
                <td><span class="rank">#${index + 1}</span></td>
                <td>
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <div class="user-avatar">${user.username.substring(0, 2).toUpperCase()}</div>
                        <div>
                            <div style="font-weight: 600;">@${user.username}</div>
                            <div style="font-size: 0.8rem; color: var(--text-dim);">
                                ${user.profile_url ? `<a href="${user.profile_url}" target="_blank" style="color: var(--primary);">View Profile</a>` : 'Profile'}
                            </div>
                        </div>
                    </div>
                </td>
                <td>
                    <span class="score-badge ${this.getScoreClass(user.avg_score)}">
                        ${user.avg_score.toFixed(3)}
                    </span>
                </td>
                <td>
                    <span class="score-badge ${this.getScoreClass(user.best_score)}">
                        ${user.best_score.toFixed(3)}
                    </span>
                </td>
                <td style="font-family: 'JetBrains Mono', monospace;">${user.tweet_count}</td>
                <td>
                    <div style="font-size: 0.8rem; color: var(--text-dim);">
                        Quality contributor
                    </div>
                </td>
            </tr>
        `).join('');
    }

    displayTweets(tweets) {
        const container = document.getElementById('tweets-container');
        if (!container) return;

        if (tweets.length === 0) {
            container.innerHTML = `
                <div style="text-align: center; padding: 3rem; color: var(--text-dim);">
                    <i class="fas fa-search" style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.5;"></i>
                    <h3>No tweets analyzed yet</h3>
                    <p>The pipeline will start collecting and analyzing Crestal mentions soon.</p>
                </div>
            `;
            return;
        }

        // Sort by score descending and show top 20
        const sortedTweets = tweets
            .sort((a, b) => (parseFloat(b.score) || 0) - (parseFloat(a.score) || 0))
            .slice(0, 20);

        container.innerHTML = sortedTweets.map(tweet => this.createTweetCard(tweet)).join('');
    }

    createTweetCard(tweet) {
        const score = parseFloat(tweet.score) || 0;
        const scoreClass = this.getScoreClass(score);
        const username = tweet.username || 'unknown';
        const text = tweet.text || 'No content';
        const engagement = tweet.engagement || {};

        return `
            <div class="tweet-card">
                <div class="tweet-header">
                    <div class="user-avatar">${username.substring(0, 2).toUpperCase()}</div>
                    <div class="user-info">
                        <h3>@${username}</h3>
                        <div class="handle">Crestal Community Member</div>
                    </div>
                    <div class="score-badge ${scoreClass}">
                        ${score.toFixed(3)}
                    </div>
                </div>
                <div class="tweet-content">
                    ${this.formatTweetText(text)}
                </div>
                <div class="tweet-metrics">
                    <div class="metric">
                        <i class="fas fa-heart"></i>
                        ${engagement.likes || 0}
                    </div>
                    <div class="metric">
                        <i class="fas fa-retweet"></i>
                        ${engagement.retweets || 0}
                    </div>
                    <div class="metric">
                        <i class="fas fa-reply"></i>
                        ${engagement.replies || 0}
                    </div>
                    <div class="metric">
                        <i class="fas fa-eye"></i>
                        ${engagement.views || 0}
                    </div>
                    ${tweet.id ? `
                    <div class="metric" style="margin-left: auto;">
                        <a href="https://twitter.com/${username}/status/${tweet.id}" target="_blank" style="color: var(--primary); text-decoration: none;">
                            <i class="fas fa-external-link-alt"></i>
                            View Tweet
                        </a>
                    </div>
                    ` : ''}
                </div>
            </div>
        `;
    }

    getScoreClass(score) {
        if (score >= 1.0) return 'score-high';
        if (score >= 0.5) return 'score-medium';
        return 'score-low';
    }

    formatTweetText(text) {
        return text
            .replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank" style="color: var(--primary);">$1</a>')
            .replace(/@(\w+)/g, '<span style="color: var(--primary);">@$1</span>')
            .replace(/#(\w+)/g, '<span style="color: var(--primary);">#$1</span>')
            .replace(/\$(\w+)/g, '<span style="color: var(--primary); font-weight: 600;">$$1</span>');
    }

    showError(message) {
        // Create or update error notification
        let errorDiv = document.getElementById('error-notification');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.id = 'error-notification';
            errorDiv.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: var(--error);
                color: white;
                padding: 1rem;
                border-radius: 8px;
                z-index: 1000;
                max-width: 300px;
            `;
            document.body.appendChild(errorDiv);
        }
        
        errorDiv.textContent = message;
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        }, 5000);
    }
}

// Global functions for button actions
async function refreshData() {
    if (window.radar) {
        await window.radar.loadData();
        await window.radar.loadLeaderboard();
    }
}

async function runPipeline() {
    const btn = event.target;
    const originalText = btn.innerHTML;
    
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Running...';
    btn.disabled = true;
    
    try {
        const response = await fetch('/api/run-pipeline', { method: 'POST' });
        const result = await response.json();
        
        if (result.success) {
            btn.innerHTML = '<i class="fas fa-check"></i> Complete!';
            // Refresh data after pipeline runs
            setTimeout(() => refreshData(), 2000);
        } else {
            btn.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Error';
        }
    } catch (error) {
        console.error('Pipeline error:', error);
        btn.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Error';
    }
    
    // Reset button after 3 seconds
    setTimeout(() => {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }, 3000);
}

function exportData() {
    // Create CSV export link
    const link = document.createElement('a');
    link.href = '/api/crestal-data?format=csv';
    link.download = `nation-radar-${new Date().toISOString().split('T')[0]}.csv`;
    link.click();
}

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    window.radar = new NationRadar();
});