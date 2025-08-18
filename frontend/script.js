// Nation Radar - User-Focused Dashboard Script

class NationRadarDashboard {
    constructor() {
        this.data = [];
        this.leaderboard = [];
        this.isLoading = false;
        this.refreshInterval = null;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.loadDashboard();
        this.startAutoRefresh();
    }
    
    setupEventListeners() {
        // Smooth scrolling for navigation
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
        
        // Add scroll effects
        window.addEventListener('scroll', this.handleScroll.bind(this));
    }
    
    handleScroll() {
        const scrolled = window.pageYOffset;
        const parallax = document.querySelector('.hero');
        if (parallax) {
            const speed = scrolled * 0.5;
            parallax.style.transform = `translateY(${speed}px)`;
        }
    }
    
    async loadDashboard() {
        try {
            this.showLoading();
            
            // Load all data in parallel
            const [dataResponse, leaderboardResponse] = await Promise.all([
                fetch('/api/crestal-data'),
                fetch('/api/leaderboard?limit=10')
            ]);
            
            const dataResult = await dataResponse.json();
            const leaderboardResult = await leaderboardResponse.json();
            
            if (dataResult.success) {
                this.data = dataResult.data || [];
                this.updateDashboard(dataResult.stats);
            }
            
            if (leaderboardResult.success) {
                this.leaderboard = leaderboardResult.leaderboard || [];
                this.renderLeaderboard();
            }
            
            this.renderTrendingContent();
            this.renderActivityFeed();
            this.updateInsights();
            
        } catch (error) {
            console.error('Failed to load dashboard:', error);
            this.showError('Failed to load dashboard data');
        } finally {
            this.hideLoading();
        }
    }
    
    updateDashboard(stats) {
        if (!stats) return;
        
        // Update hero stats
        const totalUsers = document.getElementById('total-users');
        const avgScore = document.getElementById('avg-score');
        const totalContent = document.getElementById('total-content');
        
        if (totalUsers) totalUsers.textContent = stats.unique_users || this.data.length;
        if (avgScore) avgScore.textContent = (stats.avg_score || 0).toFixed(2);
        if (totalContent) totalContent.textContent = stats.total_tweets || this.data.length;
        
        // Update last update time
        const lastUpdate = document.getElementById('last-update');
        if (lastUpdate) {
            lastUpdate.textContent = new Date().toLocaleTimeString();
        }
    }
    
    renderTrendingContent() {
        const container = document.getElementById('trending-content');
        if (!container || !this.data.length) return;
        
        // Sort by score and take top 6
        const topContent = this.data
            .sort((a, b) => (b.score || 0) - (a.score || 0))
            .slice(0, 6);
        
        container.innerHTML = topContent.map(item => `
            <div class="content-card">
                <div class="content-header">
                    <div class="content-user">
                        <div class="user-avatar">
                            ${(item.username || 'U').substring(0, 2).toUpperCase()}
                        </div>
                        <div class="user-info">
                            <h4>@${item.username || 'unknown'}</h4>
                            <p>Crestal Community</p>
                        </div>
                    </div>
                    <div class="content-score ${this.getScoreClass(item.score)}">
                        ${(item.score || 0).toFixed(2)}
                    </div>
                </div>
                <div class="content-text">
                    ${this.truncateText(item.text || 'No content', 120)}
                </div>
                <div class="content-engagement">
                    <div class="engagement-item">
                        <i class="fas fa-heart"></i>
                        <span>${item.engagement?.likes || 0}</span>
                    </div>
                    <div class="engagement-item">
                        <i class="fas fa-retweet"></i>
                        <span>${item.engagement?.retweets || 0}</span>
                    </div>
                    <div class="engagement-item">
                        <i class="fas fa-reply"></i>
                        <span>${item.engagement?.replies || 0}</span>
                    </div>
                    <div class="engagement-item">
                        <i class="fas fa-eye"></i>
                        <span>${item.engagement?.views || 0}</span>
                    </div>
                </div>
            </div>
        `).join('');
    }
    
    renderLeaderboard() {
        const container = document.getElementById('leaderboard');
        if (!container || !this.leaderboard.length) return;
        
        container.innerHTML = this.leaderboard.map((user, index) => `
            <div class="leaderboard-item">
                <div class="leaderboard-rank ${index < 3 ? 'top-3' : ''}">
                    ${index + 1}
                </div>
                <div class="leaderboard-user">
                    <div class="user-avatar">
                        ${user.username.substring(0, 2).toUpperCase()}
                    </div>
                    <div class="user-info">
                        <h4>@${user.username}</h4>
                        <p>${user.tweet_count} contributions</p>
                    </div>
                </div>
                <div class="leaderboard-score">
                    ${user.avg_score.toFixed(2)}
                </div>
            </div>
        `).join('');
    }
    
    renderActivityFeed() {
        const container = document.getElementById('activity-feed');
        if (!container || !this.data.length) return;
        
        // Take recent 5 items
        const recentActivity = this.data.slice(0, 5);
        
        container.innerHTML = recentActivity.map(item => `
            <div class="activity-item">
                <div class="activity-header">
                    <div class="activity-avatar">
                        ${(item.username || 'U').substring(0, 2).toUpperCase()}
                    </div>
                    <div class="activity-meta">
                        <h4>@${item.username || 'unknown'}</h4>
                        <p>${this.formatTimestamp(item.timestamp)}</p>
                    </div>
                </div>
                <div class="activity-content">
                    ${this.truncateText(item.text || 'No content', 200)}
                </div>
                <div class="activity-engagement">
                    <div class="engagement-item">
                        <i class="fas fa-heart"></i>
                        <span>${item.engagement?.likes || 0}</span>
                    </div>
                    <div class="engagement-item">
                        <i class="fas fa-retweet"></i>
                        <span>${item.engagement?.retweets || 0}</span>
                    </div>
                    <div class="engagement-item">
                        <i class="fas fa-reply"></i>
                        <span>${item.engagement?.replies || 0}</span>
                    </div>
                    <div class="engagement-item">
                        <i class="fas fa-star"></i>
                        <span>${(item.score || 0).toFixed(2)}</span>
                    </div>
                </div>
            </div>
        `).join('');
    }
    
    updateInsights() {
        if (!this.data.length) return;
        
        // Calculate insights
        const scores = this.data.map(item => item.score || 0);
        const avgScore = scores.reduce((a, b) => a + b, 0) / scores.length;
        
        const totalEngagement = this.data.reduce((sum, item) => {
            const engagement = item.engagement || {};
            return sum + (engagement.likes || 0) + (engagement.retweets || 0) + (engagement.replies || 0);
        }, 0);
        
        const avgEngagement = totalEngagement / this.data.length;
        const uniqueUsers = new Set(this.data.map(item => item.username)).size;
        
        // Update insight metrics
        const qualityMetric = document.getElementById('quality-metric');
        const engagementMetric = document.getElementById('engagement-metric');
        const activityMetric = document.getElementById('activity-metric');
        
        if (qualityMetric) qualityMetric.textContent = avgScore.toFixed(2);
        if (engagementMetric) engagementMetric.textContent = Math.round(avgEngagement);
        if (activityMetric) activityMetric.textContent = uniqueUsers;
        
        // Update trends (mock data for now)
        this.updateTrends();
    }
    
    updateTrends() {
        // Mock trend data - in real app this would come from historical data
        const trends = {
            quality: '+0.15',
            engagement: '+12%',
            activity: '+3'
        };
        
        const qualityTrend = document.getElementById('quality-trend');
        const engagementTrend = document.getElementById('engagement-trend');
        const activityTrend = document.getElementById('activity-trend');
        
        if (qualityTrend) qualityTrend.textContent = trends.quality;
        if (engagementTrend) engagementTrend.textContent = trends.engagement;
        if (activityTrend) activityTrend.textContent = trends.activity;
    }
    
    getScoreClass(score) {
        if (score >= 1.5) return 'score-excellent';
        if (score >= 1.0) return 'score-good';
        if (score >= 0.5) return 'score-average';
        return 'score-poor';
    }
    
    truncateText(text, maxLength) {
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength) + '...';
    }
    
    formatTimestamp(timestamp) {
        if (!timestamp) return 'Just now';
        
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
    
    showLoading() {
        this.isLoading = true;
        const overlay = document.getElementById('loading-overlay');
        if (overlay) overlay.style.display = 'flex';
    }
    
    hideLoading() {
        this.isLoading = false;
        const overlay = document.getElementById('loading-overlay');
        if (overlay) overlay.style.display = 'none';
    }
    
    showError(message) {
        // Create a simple error notification
        const errorDiv = document.createElement('div');
        errorDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #ef4444;
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            z-index: 1000;
            font-weight: 500;
        `;
        errorDiv.textContent = message;
        
        document.body.appendChild(errorDiv);
        
        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    }
    
    startAutoRefresh() {
        // Refresh data every 5 minutes
        this.refreshInterval = setInterval(() => {
            this.loadDashboard();
        }, 5 * 60 * 1000);
    }
    
    stopAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
            this.refreshInterval = null;
        }
    }
}

// Add score classes to CSS
const style = document.createElement('style');
style.textContent = `
    .score-excellent {
        background: rgba(16, 185, 129, 0.1);
        color: #10b981;
        border: 1px solid #10b981;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.875rem;
    }
    
    .score-good {
        background: rgba(59, 130, 246, 0.1);
        color: #3b82f6;
        border: 1px solid #3b82f6;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.875rem;
    }
    
    .score-average {
        background: rgba(245, 158, 11, 0.1);
        color: #f59e0b;
        border: 1px solid #f59e0b;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.875rem;
    }
    
    .score-poor {
        background: rgba(239, 68, 68, 0.1);
        color: #ef4444;
        border: 1px solid #ef4444;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.875rem;
    }
    
    .content-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 1rem;
    }
    
    .content-user {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .user-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: linear-gradient(135deg, var(--primary), var(--primary-dark));
        color: var(--white);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.875rem;
    }
    
    .user-info h4 {
        font-weight: 600;
        color: var(--gray-900);
        margin-bottom: 0.25rem;
        font-size: 0.875rem;
    }
    
    .user-info p {
        font-size: 0.75rem;
        color: var(--gray-600);
    }
    
    .content-text {
        color: var(--gray-700);
        line-height: 1.6;
        margin-bottom: 1rem;
        font-size: 0.875rem;
    }
    
    .content-engagement {
        display: flex;
        gap: 1rem;
        font-size: 0.75rem;
        color: var(--gray-500);
    }
    
    .engagement-item {
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }
    
    .engagement-item i {
        font-size: 0.75rem;
    }
`;

document.head.appendChild(style);

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new NationRadarDashboard();
});

// Add some smooth animations
document.addEventListener('DOMContentLoaded', () => {
    // Animate elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe all content sections
    document.querySelectorAll('.content-section').forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(20px)';
        section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(section);
    });
});