// Nation Radar - Advanced Dashboard JavaScript

class NationRadarDashboard {
    constructor() {
        this.apiBaseUrl = '/api';
        this.charts = {};
        this.currentData = {};
        this.updateInterval = null;
        this.notificationContainer = null;
        
        this.init();
    }

    async init() {
        try {
            this.setupEventListeners();
            this.initializeCharts();
            this.showLoadingOverlay();
            
            // Initial data load
            await this.loadDashboardData();
            
            // Start real-time updates
            this.startRealTimeUpdates();
            
            // Hide loading overlay
            this.hideLoadingOverlay();
            
            // Show welcome notification
            this.showNotification('🚀 Nation Radar Dashboard Loaded!', 'success');
            
        } catch (error) {
            console.error('Dashboard initialization failed:', error);
            this.showNotification('❌ Failed to initialize dashboard', 'error');
        }
    }

    setupEventListeners() {
        // Theme toggle
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => this.toggleTheme());
        }

        // Filter buttons
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.handleFilterClick(e));
        });

        // Tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.handleTabClick(e));
        });

        // Search functionality
        const searchInput = document.getElementById('search-input');
        const searchBtn = document.querySelector('.search-btn');
        
        if (searchInput) {
            searchInput.addEventListener('input', (e) => this.handleSearchInput(e));
            searchInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') this.performSearch();
            });
        }
        
        if (searchBtn) {
            searchBtn.addEventListener('click', () => this.performSearch());
        }

        // Refresh activity
        const refreshBtn = document.getElementById('refresh-activity');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => this.refreshActivity());
        }

        // Search filters
        const scoreFilter = document.getElementById('score-filter');
        const timeFilter = document.getElementById('time-filter');
        
        if (scoreFilter) {
            scoreFilter.addEventListener('change', () => this.applySearchFilters());
        }
        
        if (timeFilter) {
            timeFilter.addEventListener('change', () => this.applySearchFilters());
        }
    }

    initializeCharts() {
        // Quality Distribution Chart
        const qualityCtx = document.getElementById('quality-chart');
        if (qualityCtx) {
            this.charts.quality = new Chart(qualityCtx, {
                type: 'doughnut',
                data: {
                    labels: ['High Quality', 'Medium Quality', 'Low Quality'],
                    datasets: [{
                        data: [0, 0, 0],
                        backgroundColor: [
                            'rgba(16, 185, 129, 0.8)',
                            'rgba(245, 158, 11, 0.8)',
                            'rgba(239, 68, 68, 0.8)'
                        ],
                        borderColor: [
                            'rgba(16, 185, 129, 1)',
                            'rgba(245, 158, 11, 1)',
                            'rgba(239, 68, 68, 1)'
                        ],
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                color: '#ffffff',
                                font: {
                                    size: 12
                                }
                            }
                        }
                    }
                }
            });
        }

        // Engagement Trends Chart
        const engagementCtx = document.getElementById('engagement-chart');
        if (engagementCtx) {
            this.charts.engagement = new Chart(engagementCtx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Engagement Rate',
                        data: [],
                        borderColor: 'rgba(99, 102, 241, 1)',
                        backgroundColor: 'rgba(99, 102, 241, 0.1)',
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            labels: {
                                color: '#ffffff'
                            }
                        }
                    },
                    scales: {
                        x: {
                            ticks: { color: '#ffffff' },
                            grid: { color: 'rgba(255, 255, 255, 0.1)' }
                        },
                        y: {
                            ticks: { color: '#ffffff' },
                            grid: { color: 'rgba(255, 255, 255, 0.1)' }
                        }
                    }
                }
            });
        }

        // Mini charts for insight cards
        this.initializeMiniCharts();
    }

    initializeMiniCharts() {
        const miniChartIds = ['quality-mini-chart', 'engagement-mini-chart', 'activity-mini-chart'];
        
        miniChartIds.forEach(id => {
            const ctx = document.getElementById(id);
            if (ctx) {
                this.charts[id] = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: ['1h', '2h', '3h', '4h', '5h', '6h'],
                        datasets: [{
                            data: [0, 0, 0, 0, 0, 0],
                            borderColor: 'rgba(255, 255, 255, 0.8)',
                            backgroundColor: 'rgba(255, 255, 255, 0.1)',
                            tension: 0.4,
                            fill: true,
                            pointRadius: 0
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { display: false }
                        },
                        scales: {
                            x: { display: false },
                            y: { display: false }
                        }
                    }
                });
            }
        });
    }

    async loadDashboardData() {
        try {
            // Load all data in parallel
            const [crestalData, leaderboard, systemStatus] = await Promise.all([
                this.fetchData('/crestal-data'),
                this.fetchData('/leaderboard'),
                this.fetchData('/system-status')
            ]);

            this.currentData = {
                crestal: crestalData,
                leaderboard: leaderboard,
                systemStatus: systemStatus
            };

            // Update UI with data
            this.updateDashboard();
            
        } catch (error) {
            console.error('Failed to load dashboard data:', error);
            this.showNotification('❌ Failed to load dashboard data', 'error');
        }
    }

    async fetchData(endpoint) {
        try {
            const response = await fetch(`${this.apiBaseUrl}${endpoint}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error(`Error fetching ${endpoint}:`, error);
            throw error;
        }
    }

    updateDashboard() {
        this.updateHeroStats();
        this.updateTrendingContent();
        this.updateInsights();
        this.updateLeaderboard();
        this.updateActivityFeed();
        this.updateCharts();
        this.updateFooter();
    }

    updateHeroStats() {
        const { systemStatus } = this.currentData;
        
        if (systemStatus?.success) {
            const stats = systemStatus.statistics;
            
            // Update stat numbers with animation
            this.animateNumber('total-users', stats.total_tweets || 0);
            this.animateNumber('avg-score', stats.average_score || 0);
            this.animateNumber('total-content', stats.scored_tweets || 0);
        }
    }

    updateTrendingContent() {
        const { crestal } = this.currentData;
        const container = document.getElementById('trending-content');
        
        if (!container || !crestal?.success) return;

        container.innerHTML = '';
        
        crestal.data?.forEach((tweet, index) => {
            const card = this.createContentCard(tweet, index);
            container.appendChild(card);
        });
    }

    createContentCard(tweet, index) {
        const card = document.createElement('div');
        card.className = 'content-card glass-effect fade-in';
        card.style.animationDelay = `${index * 0.1}s`;
        
        const engagement = tweet.engagement || {};
        const totalEngagement = (engagement.likes || 0) + (engagement.retweets || 0) + (engagement.replies || 0);
        
        card.innerHTML = `
            <div class="card-header">
                <div class="user-info">
                    <div class="user-avatar">
                        <i class="fas fa-user"></i>
                    </div>
                    <div>
                        <h4>@${tweet.username}</h4>
                        <span class="timestamp">${this.formatTimestamp(tweet.created_at)}</span>
                    </div>
                </div>
                <div class="score-badge" style="background: ${this.getScoreColor(tweet.score)}">
                    ${tweet.score.toFixed(3)}
                </div>
            </div>
            <div class="card-content">
                <p>${this.truncateText(tweet.text, 150)}</p>
            </div>
            <div class="card-footer">
                <div class="engagement-stats">
                    <span><i class="fas fa-heart"></i> ${engagement.likes || 0}</span>
                    <span><i class="fas fa-retweet"></i> ${engagement.retweets || 0}</span>
                    <span><i class="fas fa-comment"></i> ${engagement.replies || 0}</span>
                    <span><i class="fas fa-eye"></i> ${engagement.views || 0}</span>
                </div>
                <div class="total-engagement">
                    Total: ${totalEngagement}
                </div>
            </div>
        `;
        
        return card;
    }

    updateInsights() {
        const { systemStatus, crestal } = this.currentData;
        
        if (systemStatus?.success) {
            const stats = systemStatus.statistics;
            
            // Update quality metric
            this.updateInsightMetric('quality-metric', stats.average_score || 0);
            this.updateInsightMetric('quality-trend', '+8%');
            
            // Update engagement metric
            const avgEngagement = this.calculateAverageEngagement(crestal?.data || []);
            this.updateInsightMetric('engagement-metric', avgEngagement);
            this.updateInsightMetric('engagement-trend', '+12%');
            
            // Update activity metric
            this.updateInsightMetric('activity-metric', stats.scored_tweets || 0);
            this.updateInsightMetric('activity-trend', '+24%');
        }
    }

    updateLeaderboard() {
        const { leaderboard } = this.currentData;
        const container = document.getElementById('leaderboard');
        
        if (!container || !leaderboard?.success) return;

        container.innerHTML = '';
        
        leaderboard.data?.forEach((tweet, index) => {
            const item = this.createLeaderboardItem(tweet, index);
            container.appendChild(item);
        });
    }

    createLeaderboardItem(tweet, index) {
        const item = document.createElement('div');
        item.className = 'leaderboard-item glass-effect fade-in';
        item.style.animationDelay = `${index * 0.1}s`;
        
        const rankClass = index < 3 ? 'top-3' : '';
        const rankIcon = index < 3 ? ['🥇', '🥈', '🥉'][index] : (index + 1);
        
        item.innerHTML = `
            <div class="leaderboard-rank ${rankClass}">
                ${rankIcon}
            </div>
            <div class="leaderboard-user">
                <div class="user-avatar">
                    <i class="fas fa-user"></i>
                </div>
                <div class="user-info">
                    <h4>@${tweet.username}</h4>
                    <p>${this.truncateText(tweet.text, 100)}</p>
                </div>
            </div>
            <div class="leaderboard-score">
                ${tweet.score.toFixed(3)}
            </div>
        `;
        
        return item;
    }

    updateActivityFeed() {
        const { crestal } = this.currentData;
        const container = document.getElementById('activity-feed');
        
        if (!container || !crestal?.success) return;

        container.innerHTML = '';
        
        crestal.data?.slice(0, 5).forEach((tweet, index) => {
            const item = this.createActivityItem(tweet, index);
            container.appendChild(item);
        });
    }

    createActivityItem(tweet, index) {
        const item = document.createElement('div');
        item.className = 'activity-item glass-effect fade-in';
        item.style.animationDelay = `${index * 0.1}s`;
        
        item.innerHTML = `
            <div class="activity-header">
                <div class="activity-avatar">
                    <i class="fas fa-user"></i>
                </div>
                <div class="activity-meta">
                    <h4>@${tweet.username}</h4>
                    <p>${this.formatTimestamp(tweet.created_at)}</p>
                </div>
                <div class="activity-score">
                    ${tweet.score.toFixed(3)}
                </div>
            </div>
            <div class="activity-content">
                ${this.truncateText(tweet.text, 120)}
            </div>
        `;
        
        return item;
    }

    updateCharts() {
        const { crestal } = this.currentData;
        
        if (!crestal?.success) return;

        // Update quality distribution chart
        if (this.charts.quality) {
            const qualityData = this.calculateQualityDistribution(crestal.data);
            this.charts.quality.data.datasets[0].data = qualityData;
            this.charts.quality.update();
        }

        // Update engagement trends chart
        if (this.charts.engagement) {
            const engagementData = this.calculateEngagementTrends(crestal.data);
            this.charts.engagement.data.labels = engagementData.labels;
            this.charts.engagement.data.datasets[0].data = engagementData.data;
            this.charts.engagement.update();
        }

        // Update mini charts
        this.updateMiniCharts();
    }

    updateMiniCharts() {
        // Simulate real-time data for mini charts
        const mockData = Array.from({length: 6}, () => Math.random() * 100);
        
        Object.values(this.charts).forEach(chart => {
            if (chart.options.scales?.x?.display === false) { // Mini chart
                chart.data.datasets[0].data = mockData;
                chart.update('none');
            }
        });
    }

    updateFooter() {
        const { systemStatus } = this.currentData;
        
        if (systemStatus?.success) {
            this.updateElement('last-update', this.formatTimestamp(systemStatus.timestamp));
            this.updateElement('api-calls', Math.floor(Math.random() * 1000) + 100);
            this.updateElement('response-time', Math.floor(Math.random() * 50) + 10);
        }
    }

    // Utility methods
    animateNumber(elementId, targetValue) {
        const element = document.getElementById(elementId);
        if (!element) return;

        const startValue = parseFloat(element.textContent) || 0;
        const duration = 1000;
        const startTime = performance.now();

        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const currentValue = startValue + (targetValue - startValue) * this.easeOutQuart(progress);
            element.textContent = currentValue.toFixed(3);
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };

        requestAnimationFrame(animate);
    }

    easeOutQuart(t) {
        return 1 - Math.pow(1 - t, 4);
    }

    updateElement(elementId, value) {
        const element = document.getElementById(elementId);
        if (element) {
            element.textContent = value;
        }
    }

    updateInsightMetric(metricId, value) {
        const element = document.getElementById(metricId);
        if (element) {
            if (metricId.includes('metric')) {
                this.animateNumber(metricId, value);
            } else {
                element.textContent = value;
            }
        }
    }

    formatTimestamp(timestamp) {
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

    truncateText(text, maxLength) {
        if (!text) return '';
        return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
    }

    getScoreColor(score) {
        if (score >= 0.8) return 'linear-gradient(135deg, #10b981, #059669)';
        if (score >= 0.4) return 'linear-gradient(135deg, #f59e0b, #d97706)';
        return 'linear-gradient(135deg, #ef4444, #dc2626)';
    }

    calculateAverageEngagement(tweets) {
        if (!tweets.length) return 0;
        
        const totalEngagement = tweets.reduce((sum, tweet) => {
            const engagement = tweet.engagement || {};
            return sum + (engagement.likes || 0) + (engagement.retweets || 0) + (engagement.replies || 0);
        }, 0);
        
        return Math.round(totalEngagement / tweets.length);
    }

    calculateQualityDistribution(tweets) {
        const distribution = [0, 0, 0]; // High, Medium, Low
        
        tweets.forEach(tweet => {
            if (tweet.score >= 0.8) distribution[0]++;
            else if (tweet.score >= 0.4) distribution[1]++;
            else distribution[2]++;
        });
        
        return distribution;
    }

    calculateEngagementTrends(tweets) {
        // Simulate time-based engagement data
        const labels = ['1h ago', '2h ago', '3h ago', '4h ago', '5h ago', '6h ago'];
        const data = labels.map(() => Math.floor(Math.random() * 100) + 20);
        
        return { labels, data };
    }

    // Event handlers
    handleFilterClick(event) {
        const btn = event.target;
        const filter = btn.dataset.filter;
        
        // Update active state
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        // Apply filter
        this.applyContentFilter(filter);
    }

    handleTabClick(event) {
        const btn = event.target;
        const tab = btn.dataset.tab;
        
        // Update active state
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        // Apply tab filter
        this.applyLeaderboardTab(tab);
    }

    handleSearchInput(event) {
        const query = event.target.value.trim();
        if (query.length >= 2) {
            this.debounceSearch(query);
        }
    }

    async performSearch() {
        const query = document.getElementById('search-input')?.value.trim();
        if (!query) return;

        try {
            const results = await this.fetchData(`/search?q=${encodeURIComponent(query)}`);
            this.displaySearchResults(results);
        } catch (error) {
            console.error('Search failed:', error);
            this.showNotification('❌ Search failed', 'error');
        }
    }

    displaySearchResults(results) {
        const container = document.getElementById('search-results');
        if (!container) return;

        if (!results.success || !results.results?.length) {
            container.innerHTML = '<p class="no-results">No results found</p>';
            return;
        }

        container.innerHTML = results.results.map(tweet => `
            <div class="search-result-item glass-effect">
                <div class="result-header">
                    <span class="username">@${tweet.username}</span>
                    <span class="score">${tweet.score.toFixed(3)}</span>
                </div>
                <p class="result-text">${this.truncateText(tweet.text, 200)}</p>
                <div class="result-meta">
                    <span>${this.formatTimestamp(tweet.created_at)}</span>
                    <span>❤️ ${tweet.engagement?.likes || 0}</span>
                </div>
            </div>
        `).join('');
    }

    applyContentFilter(filter) {
        const { crestal } = this.currentData;
        if (!crestal?.success) return;

        let filteredData = crestal.data;

        switch (filter) {
            case 'high-score':
                filteredData = filteredData.filter(tweet => tweet.score >= 0.8);
                break;
            case 'high-engagement':
                filteredData = filteredData.filter(tweet => {
                    const engagement = tweet.engagement || {};
                    const total = (engagement.likes || 0) + (engagement.retweets || 0) + (engagement.replies || 0);
                    return total > 10;
                });
                break;
        }

        // Update trending content with filtered data
        const container = document.getElementById('trending-content');
        if (container) {
            container.innerHTML = '';
            filteredData.forEach((tweet, index) => {
                const card = this.createContentCard(tweet, index);
                container.appendChild(card);
            });
        }
    }

    applyLeaderboardTab(tab) {
        const { leaderboard } = this.currentData;
        if (!leaderboard?.success) return;

        let sortedData = [...leaderboard.data];

        switch (tab) {
            case 'engagement':
                sortedData.sort((a, b) => {
                    const aEngagement = (a.engagement?.likes || 0) + (a.engagement?.retweets || 0) + (a.engagement?.replies || 0);
                    const bEngagement = (b.engagement?.likes || 0) + (b.engagement?.retweets || 0) + (b.engagement?.replies || 0);
                    return bEngagement - aEngagement;
                });
                break;
            case 'activity':
                sortedData.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
                break;
            default: // score
                sortedData.sort((a, b) => b.score - a.score);
        }

        // Update leaderboard display
        const container = document.getElementById('leaderboard');
        if (container) {
            container.innerHTML = '';
            sortedData.forEach((tweet, index) => {
                const item = this.createLeaderboardItem(tweet, index);
                container.appendChild(item);
            });
        }
    }

    applySearchFilters() {
        // Apply score and time filters to search results
        this.performSearch();
    }

    async refreshActivity() {
        try {
            await this.loadDashboardData();
            this.showNotification('🔄 Activity refreshed!', 'success');
        } catch (error) {
            this.showNotification('❌ Failed to refresh activity', 'error');
        }
    }

    // Theme management
    toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        
        const icon = document.querySelector('#theme-toggle i');
        if (icon) {
            icon.className = newTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
        }
        
        // Save theme preference
        localStorage.setItem('theme', newTheme);
        
        this.showNotification(`🌙 Theme switched to ${newTheme}`, 'info');
    }

    // Real-time updates
    startRealTimeUpdates() {
        this.updateInterval = setInterval(async () => {
            try {
                await this.loadDashboardData();
                this.updateCharts();
            } catch (error) {
                console.error('Real-time update failed:', error);
            }
        }, 30000); // Update every 30 seconds
    }

    // Loading overlay management
    showLoadingOverlay() {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.style.display = 'flex';
        }
    }

    hideLoadingOverlay() {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.style.display = 'none';
        }
    }

    // Notification system
    showNotification(message, type = 'info') {
        if (!this.notificationContainer) {
            this.notificationContainer = document.getElementById('notification-container');
        }

        const notification = document.createElement('div');
        notification.className = `notification notification-${type} glass-effect fade-in`;
        
        const icon = this.getNotificationIcon(type);
        
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-icon">${icon}</span>
                <span class="notification-message">${message}</span>
            </div>
            <button class="notification-close">
                <i class="fas fa-times"></i>
            </button>
        `;

        // Add close functionality
        const closeBtn = notification.querySelector('.notification-close');
        closeBtn.addEventListener('click', () => {
            notification.remove();
        });

        this.notificationContainer.appendChild(notification);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }

    getNotificationIcon(type) {
        const icons = {
            success: '✅',
            error: '❌',
            warning: '⚠️',
            info: 'ℹ️'
        };
        return icons[type] || icons.info;
    }

    // Utility methods
    debounceSearch(query) {
        clearTimeout(this.searchTimeout);
        this.searchTimeout = setTimeout(() => {
            this.performSearch();
        }, 500);
    }

    // Cleanup
    destroy() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
        }
        
        // Destroy charts
        Object.values(this.charts).forEach(chart => {
            if (chart && typeof chart.destroy === 'function') {
                chart.destroy();
            }
        });
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Load saved theme
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    
    // Update theme toggle icon
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        const icon = themeToggle.querySelector('i');
        if (icon) {
            icon.className = savedTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
        }
    }
    
    // Initialize dashboard
    window.nationRadarDashboard = new NationRadarDashboard();
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (window.nationRadarDashboard) {
        window.nationRadarDashboard.destroy();
    }
});