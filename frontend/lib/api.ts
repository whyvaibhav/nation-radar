// API service for Nation Radar backend
// Updated to connect to VPS at 143.198.226.161:5000
// Last updated: 2025-08-20 20:00 UTC - Force rebuild
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'https://143.198.226.161:5000';

console.log('🔗 API Base URL:', API_BASE);
console.log('🕐 Build timestamp:', new Date().toISOString());

export interface Tweet {
  id: string;
  text: string;
  username: string;
  score: number;
  created_at: string;
  engagement: {
    likes: number;
    retweets: number;
    replies: number;
    views: number;
    bookmarks: number;
    quote_tweets: number;
  };
}

export interface SystemStats {
  total_tweets: number;
  recent_tweets_24h: number;
  average_score: number;
  top_score: number;
  last_updated: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  count: number;
  timestamp: string;
}

class ApiService {
  private async fetchApi<T>(endpoint: string): Promise<T> {
    try {
      const url = `${API_BASE}${endpoint}`;
      console.log('🌐 Fetching from:', url);
      
      const response = await fetch(url);
      
      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('✅ API Response:', data);
      return data;
    } catch (error) {
      console.error(`❌ Failed to fetch ${endpoint}:`, error);
      throw error;
    }
  }

  async getTweets(limit: number = 50): Promise<ApiResponse<Tweet[]>> {
    try {
      const response = await this.fetchApi<any>(`/api/crestal-data?limit=${limit}`);
      
      // Transform backend response to match frontend expectations
      if (response.success && response.data) {
        const transformedData: Tweet[] = response.data.map((item: any) => ({
          id: item.id || 'unknown',
          text: item.text || '',
          username: item.username || 'unknown',
          score: typeof item.score === 'number' ? item.score : 0,
          created_at: item.created_at || new Date().toISOString(),
          engagement: {
            likes: item.engagement?.likes || 0,
            retweets: item.engagement?.retweets || 0,
            replies: item.engagement?.replies || 0,
            views: item.engagement?.views || 0,
            bookmarks: item.engagement?.bookmarks || 0,
            quote_tweets: item.engagement?.quote_tweets || 0
          }
        }));

        return {
          success: true,
          data: transformedData,
          count: transformedData.length,
          timestamp: new Date().toISOString()
        };
      }
      
      return this.getDemoTweetsData();
    } catch (error) {
      console.error('❌ API failed, using demo data:', error);
      return this.getDemoTweetsData();
    }
  }

  private getDemoTweetsData(): ApiResponse<Tweet[]> {
    return {
      success: true,
      data: [
        {
          id: "demo1",
          text: "🚀 Crestal Network is revolutionizing the future of social media! #Crestal #Innovation",
          username: "crestal_enthusiast",
          score: 1.8,
          created_at: new Date().toISOString(),
          engagement: { likes: 45, retweets: 12, replies: 8, views: 1200, bookmarks: 5, quote_tweets: 3 }
        },
        {
          id: "demo2", 
          text: "Just discovered the amazing community at @crestalnetwork! The engagement is incredible! 🔥",
          username: "social_explorer",
          score: 1.6,
          created_at: new Date().toISOString(),
          engagement: { likes: 32, retweets: 9, replies: 6, views: 890, bookmarks: 4, quote_tweets: 2 }
        }
      ],
      count: 2,
      timestamp: new Date().toISOString()
    };
  }

  async getLeaderboard(limit: number = 20): Promise<ApiResponse<Tweet[]>> {
    try {
      const response = await this.fetchApi<any>(`/api/leaderboard?limit=${limit}`);
      
      // Transform leaderboard response to Tweet format expected by frontend
      if (response.success && response.leaderboard) {
        const transformedData: Tweet[] = response.leaderboard.map((user: any, index: number) => ({
          id: `leaderboard_${user.username}_${index}`,
          text: `🏆 Rank #${user.rank || index + 1}: ${user.tweet_count} high-quality tweets with avg score ${user.avg_score.toFixed(2)}`,
          username: user.username,
          score: user.avg_score || user.best_score || 0,
          created_at: new Date().toISOString(),
          engagement: {
            likes: Math.round(user.avg_score * 20), // Simulate engagement based on score
            retweets: Math.round(user.avg_score * 8),
            replies: Math.round(user.avg_score * 5),
            views: Math.round(user.avg_score * 100),
            bookmarks: Math.round(user.avg_score * 3),
            quote_tweets: Math.round(user.avg_score * 2)
          }
        }));

        return {
          success: true,
          data: transformedData,
          count: transformedData.length,
          timestamp: new Date().toISOString()
        };
      }
      
      return this.getDemoLeaderboardData();
    } catch (error) {
      console.log('Leaderboard API failed, using demo data');
      return this.getDemoLeaderboardData();
    }
  }

  private getDemoLeaderboardData(): ApiResponse<Tweet[]> {
    return {
      success: true,
      data: [
        {
          id: "top1",
          text: "🏆 Top contributor to the Crestal community! Building the future together!",
          username: "crestal_champion",
          score: 2.0,
          created_at: new Date().toISOString(),
          engagement: { likes: 89, retweets: 23, replies: 15, views: 2500, bookmarks: 12, quote_tweets: 8 }
        }
      ],
      count: 1,
      timestamp: new Date().toISOString()
    };
  }

  async getSystemStats(): Promise<{ statistics: SystemStats }> {
    try {
      // Use crestal-data endpoint directly since it has the real stats
      const dataResponse = await this.fetchApi<any>('/api/crestal-data?limit=1');
      
      if (dataResponse.success && dataResponse.stats) {
        const stats = {
          total_tweets: dataResponse.stats.total_tweets || 0,
          recent_tweets_24h: Math.round((dataResponse.stats.total_tweets || 0) * 0.1), // Estimate 10% recent
          average_score: dataResponse.stats.avg_score || 0,
          top_score: dataResponse.stats.high_quality ? 2.0 : dataResponse.stats.avg_score * 1.5 || 0,
          last_updated: new Date().toISOString()
        };
        return { statistics: stats };
      }
      
      return this.getDemoStatsData();
    } catch (error) {
      console.error('❌ Stats API failed, using demo data:', error);
      return this.getDemoStatsData();
    }
  }

  private getDemoStatsData(): { statistics: SystemStats } {
    return {
      statistics: {
        total_tweets: 156,
        recent_tweets_24h: 23,
        average_score: 1.4,
        top_score: 2.0,
        last_updated: new Date().toISOString()
      }
    };
  }

  async searchTweets(query: string, limit: number = 50): Promise<ApiResponse<Tweet[]>> {
    return this.fetchApi<ApiResponse<Tweet[]>>(`/api/search?q=${encodeURIComponent(query)}&limit=${limit}`);
  }
}

export const apiService = new ApiService();
