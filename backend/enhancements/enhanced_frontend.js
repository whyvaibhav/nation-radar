// Enhanced frontend features for Vercel deployment
// Add these functions to your frontend/script.js

class EnhancedLeaderboard {
    constructor() {
        this.currentView = 'overall';
    }

    async loadEnhancedLeaderboards() {
        try {
            const response = await fetch('/api/enhanced-leaderboards');
            const result = await response.json();
            
            if (result.success) {
                this.displayMultiDimensionalLeaderboards(result.leaderboards);
            }
        } catch (error) {
            console.error('Failed to load enhanced leaderboards:', error);
        }
    }

    displayMultiDimensionalLeaderboards(leaderboards) {
        const container = document.getElementById('leaderboards-container');
        
        container.innerHTML = `
            <div class="leaderboard-tabs">
                <button class="tab-btn active" onclick="showLeaderboard('overall')">
                    🏆 Overall Excellence
                </button>
                <button class="tab-btn" onclick="showLeaderboard('rising')">
                    🚀 Rising Stars
                </button>
                <button class="tab-btn" onclick="showLeaderboard('consistency')">
                    💎 Consistency Champions
                </button>
                <button class="tab-btn" onclick="showLeaderboard('insights')">
                    📊 Community Insights
                </button>
            </div>
            
            <div id="overall-leaderboard" class="leaderboard-content">
                ${this.renderOverallLeaderboard(leaderboards.overall_excellence)}
            </div>
            
            <div id="rising-leaderboard" class="leaderboard-content hidden">
                ${this.renderRisingStars(leaderboards.rising_stars)}
            </div>
            
            <div id="consistency-leaderboard" class="leaderboard-content hidden">
                ${this.renderConsistencyChampions(leaderboards.consistency_champions)}
            </div>
            
            <div id="insights-content" class="leaderboard-content hidden">
                ${this.renderCommunityInsights(leaderboards.content_insights)}
            </div>
        `;
    }

    renderOverallLeaderboard(users) {
        return `
            <div class="leaderboard-header">
                <h3>🏆 Top Crestal Contributors</h3>
                <p>Ranked by average quality score</p>
            </div>
            <div class="leaderboard-list">
                ${users.map((user, index) => `
                    <div class="leaderboard-item ${this.getScoreClass(user.avg_score)}">
                        <div class="rank">#${index + 1}</div>
                        <div class="user-info">
                            <a href="${user.profile_url}" target="_blank" class="username">
                                @${user.username}
                            </a>
                            <div class="user-stats">
                                <span class="stat">
                                    <i class="fas fa-chart-line"></i> ${user.avg_score} avg
                                </span>
                                <span class="stat">
                                    <i class="fas fa-star"></i> ${user.best_score} best
                                </span>
                                <span class="stat">
                                    <i class="fas fa-comment"></i> ${user.tweet_count} tweets
                                </span>
                            </div>
                        </div>
                        <div class="achievements">
                            ${this.getUserAchievements(user.username)}
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    renderRisingStars(users) {
        return `
            <div class="leaderboard-header">
                <h3>🚀 Rising Stars</h3>
                <p>Users with the biggest improvement</p>
            </div>
            <div class="leaderboard-list">
                ${users.map((user, index) => `
                    <div class="leaderboard-item rising-star">
                        <div class="rank">#${index + 1}</div>
                        <div class="user-info">
                            <a href="${user.profile_url}" target="_blank" class="username">
                                @${user.username}
                            </a>
                            <div class="improvement-stats">
                                <span class="improvement">
                                    <i class="fas fa-arrow-up"></i> +${user.improvement} improvement
                                </span>
                                <span class="current">
                                    Current avg: ${user.current_avg}
                                </span>
                                <span class="tweets">
                                    ${user.total_tweets} tweets
                                </span>
                            </div>
                        </div>
                        <div class="trend-indicator">
                            <div class="trend-arrow">📈</div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    renderConsistencyChampions(users) {
        return `
            <div class="leaderboard-header">
                <h3>💎 Consistency Champions</h3>
                <p>Most reliable quality contributors</p>
            </div>
            <div class="leaderboard-list">
                ${users.map((user, index) => `
                    <div class="leaderboard-item consistency-champion">
                        <div class="rank">#${index + 1}</div>
                        <div class="user-info">
                            <div class="username">@${user.username}</div>
                            <div class="consistency-stats">
                                <span class="consistency">
                                    <i class="fas fa-bullseye"></i> ${user.consistency_score} consistency
                                </span>
                                <span class="avg">
                                    <i class="fas fa-chart-line"></i> ${user.avg_score} avg
                                </span>
                                <span class="tweets">
                                    <i class="fas fa-comment"></i> ${user.tweet_count} tweets
                                </span>
                            </div>
                        </div>
                        <div class="consistency-badge">💎</div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    renderCommunityInsights(insights) {
        return `
            <div class="community-insights">
                <h3>📊 Community Health Dashboard</h3>
                
                <div class="insights-grid">
                    <div class="insight-card">
                        <h4>📈 Quality Trends</h4>
                        <div class="metric">
                            <span class="value">${insights.high_quality_percent}%</span>
                            <span class="label">High Quality Content</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress" style="width: ${insights.high_quality_percent}%"></div>
                        </div>
                    </div>
                    
                    <div class="insight-card">
                        <h4>🎯 Content Performance</h4>
                        <div class="content-analysis">
                            <div class="length-insight">
                                <span class="label">Short Tweets:</span>
                                <span class="value">${insights.length_vs_quality.short_tweets_avg}</span>
                            </div>
                            <div class="length-insight">
                                <span class="label">Medium Tweets:</span>
                                <span class="value">${insights.length_vs_quality.medium_tweets_avg}</span>
                            </div>
                            <div class="length-insight">
                                <span class="label">Long Tweets:</span>
                                <span class="value">${insights.length_vs_quality.long_tweets_avg}</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="insight-card">
                        <h4>🏆 Overall Stats</h4>
                        <div class="overall-stats">
                            <div class="stat">
                                <span class="value">${insights.total_tweets}</span>
                                <span class="label">Total Tweets</span>
                            </div>
                            <div class="stat">
                                <span class="value">${insights.avg_score}</span>
                                <span class="label">Average Score</span>
                            </div>
                            <div class="stat">
                                <span class="value">${Math.round(insights.avg_length)}</span>
                                <span class="label">Avg Length</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    async getUserAchievements(username) {
        try {
            const response = await fetch(`/api/user-trends/${username}`);
            const result = await response.json();
            
            if (result.success && result.user_data.achievements) {
                return result.user_data.achievements.slice(0, 3).map(achievement => 
                    `<span class="achievement" title="${achievement}">${achievement.split(' ')[0]}</span>`
                ).join('');
            }
        } catch (error) {
            console.error('Failed to load achievements:', error);
        }
        return '';
    }

    getScoreClass(score) {
        if (score >= 1.8) return 'score-legendary';
        if (score >= 1.5) return 'score-excellent';
        if (score >= 1.0) return 'score-good';
        if (score >= 0.5) return 'score-average';
        return 'score-poor';
    }
}

// Tab switching functionality
function showLeaderboard(type) {
    // Hide all content
    document.querySelectorAll('.leaderboard-content').forEach(content => {
        content.classList.add('hidden');
    });
    
    // Remove active class from all tabs
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected content
    document.getElementById(`${type}-leaderboard`).classList.remove('hidden');
    if (type === 'insights') {
        document.getElementById('insights-content').classList.remove('hidden');
    }
    
    // Add active class to clicked tab
    event.target.classList.add('active');
}

// Initialize enhanced leaderboard
document.addEventListener('DOMContentLoaded', function() {
    const enhancedLeaderboard = new EnhancedLeaderboard();
    enhancedLeaderboard.loadEnhancedLeaderboards();
});
