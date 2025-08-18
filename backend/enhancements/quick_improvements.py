#!/usr/bin/env python3
"""
Quick Implementation Examples for Crestal Monitor Improvements
High-impact enhancements you can add immediately
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict

class CrestalAnalytics:
    """Enhanced analytics for the Crestal monitoring system"""
    
    def __init__(self, csv_filename='groktweets.csv'):
        self.csv_filename = csv_filename
    
    def get_user_trends(self, username, days=30):
        """Analyze user's score trends over time"""
        df = pd.read_csv(self.csv_filename, header=None)
        df.columns = ['id', 'username', 'text', 'score', 'profile_url']
        
        user_data = df[df['username'] == username].copy()
        if len(user_data) == 0:
            return None
            
        user_data['score'] = pd.to_numeric(user_data['score'], errors='coerce')
        
        # Calculate trends
        scores = user_data['score'].tolist()
        trend = "↗️ Improving" if len(scores) > 1 and scores[-1] > scores[0] else "➡️ Stable"
        consistency = np.std(scores) if len(scores) > 1 else 0
        
        return {
            'username': username,
            'total_tweets': len(scores),
            'avg_score': round(np.mean(scores), 2),
            'best_score': max(scores),
            'worst_score': min(scores),
            'trend': trend,
            'consistency_score': round(1 - min(consistency, 1), 2),  # Higher = more consistent
            'improvement_rate': round((scores[-1] - scores[0]) / len(scores), 3) if len(scores) > 1 else 0
        }
    
    def get_rising_stars(self, min_tweets=3):
        """Find users with rapidly improving scores"""
        df = pd.read_csv(self.csv_filename, header=None)
        df.columns = ['id', 'username', 'text', 'score', 'profile_url']
        df['score'] = pd.to_numeric(df['score'], errors='coerce')
        
        rising_stars = []
        for username in df['username'].unique():
            user_data = df[df['username'] == username]
            if len(user_data) >= min_tweets:
                scores = user_data['score'].tolist()
                if len(scores) >= 3:
                    # Calculate improvement rate
                    recent_avg = np.mean(scores[-3:])  # Last 3 tweets
                    early_avg = np.mean(scores[:3])    # First 3 tweets
                    improvement = recent_avg - early_avg
                    
                    if improvement > 0.2:  # Significant improvement
                        rising_stars.append({
                            'username': username,
                            'improvement': round(improvement, 2),
                            'current_avg': round(recent_avg, 2),
                            'total_tweets': len(scores),
                            'profile_url': user_data['profile_url'].iloc[0]
                        })
        
        return sorted(rising_stars, key=lambda x: x['improvement'], reverse=True)[:10]
    
    def get_content_insights(self):
        """Analyze content patterns and quality"""
        df = pd.read_csv(self.csv_filename, header=None)
        df.columns = ['id', 'username', 'text', 'score', 'profile_url']
        df['score'] = pd.to_numeric(df['score'], errors='coerce')
        
        # Analyze content length vs score
        df['text_length'] = df['text'].str.len()
        
        insights = {
            'total_tweets': len(df),
            'avg_score': round(df['score'].mean(), 2),
            'high_quality_percent': round(len(df[df['score'] >= 1.0]) / len(df) * 100, 1),
            'avg_length': round(df['text_length'].mean(), 0),
            'length_vs_quality': {
                'short_tweets_avg': round(df[df['text_length'] < 100]['score'].mean(), 2),
                'medium_tweets_avg': round(df[(df['text_length'] >= 100) & (df['text_length'] < 250)]['score'].mean(), 2),
                'long_tweets_avg': round(df[df['text_length'] >= 250]['score'].mean(), 2)
            }
        }
        
        return insights
    
    def get_achievements(self, username):
        """Check user achievements"""
        df = pd.read_csv(self.csv_filename, header=None)
        df.columns = ['id', 'username', 'text', 'score', 'profile_url']
        df['score'] = pd.to_numeric(df['score'], errors='coerce')
        
        user_data = df[df['username'] == username]
        if len(user_data) == 0:
            return []
        
        scores = user_data['score'].tolist()
        achievements = []
        
        # Check various achievements
        if max(scores) >= 1.5:
            achievements.append("🌟 Quality Pioneer - First tweet over 1.5 score")
        
        if len(scores) >= 5 and all(s >= 1.0 for s in scores[-5:]):
            achievements.append("🔥 Hot Streak - 5 consecutive quality tweets")
        
        if len(scores) >= 10 and np.std(scores) < 0.2:
            achievements.append("🎯 Consistency Champion - Reliable quality")
        
        if np.mean(scores) >= 1.8 and len(scores) >= 20:
            achievements.append("💎 Diamond Contributor - Elite status")
        
        if len(scores) >= 10:
            recent_avg = np.mean(scores[-5:])
            early_avg = np.mean(scores[:5])
            if recent_avg - early_avg >= 0.5:
                achievements.append("📈 Improvement Master - Major score growth")
        
        return achievements

class EnhancedLeaderboard:
    """Enhanced leaderboard with multiple ranking systems"""
    
    def __init__(self, csv_filename='groktweets.csv'):
        self.csv_filename = csv_filename
        self.analytics = CrestalAnalytics(csv_filename)
    
    def get_multi_dimensional_rankings(self):
        """Get various leaderboard rankings"""
        df = pd.read_csv(self.csv_filename, header=None)
        df.columns = ['id', 'username', 'text', 'score', 'profile_url']
        df['score'] = pd.to_numeric(df['score'], errors='coerce')
        
        # Overall excellence (existing)
        overall = df.groupby('username').agg({
            'score': ['mean', 'max', 'count'],
            'profile_url': 'first'
        }).round(2)
        overall.columns = ['avg_score', 'best_score', 'tweet_count', 'profile_url']
        overall = overall.reset_index().sort_values('avg_score', ascending=False).head(10)
        
        # Rising stars
        rising_stars = self.analytics.get_rising_stars()
        
        # Consistency kings (low standard deviation)
        consistency = []
        for username in df['username'].unique():
            user_scores = df[df['username'] == username]['score'].tolist()
            if len(user_scores) >= 5:  # Minimum tweets for consistency
                std_dev = np.std(user_scores)
                consistency.append({
                    'username': username,
                    'consistency_score': round(1 - min(std_dev, 1), 2),
                    'avg_score': round(np.mean(user_scores), 2),
                    'tweet_count': len(user_scores)
                })
        consistency = sorted(consistency, key=lambda x: x['consistency_score'], reverse=True)[:10]
        
        return {
            'overall_excellence': overall.to_dict('records'),
            'rising_stars': rising_stars,
            'consistency_champions': consistency,
            'content_insights': self.analytics.get_content_insights()
        }

# Usage examples:
if __name__ == "__main__":
    # Initialize analytics
    analytics = CrestalAnalytics()
    leaderboard = EnhancedLeaderboard()
    
    # Example usage:
    print("🔥 Rising Stars:")
    rising = analytics.get_rising_stars()
    for i, user in enumerate(rising[:5], 1):
        print(f"{i}. @{user['username']} (+{user['improvement']} improvement)")
    
    print("\n📊 Content Insights:")
    insights = analytics.get_content_insights()
    print(f"Quality Rate: {insights['high_quality_percent']}%")
    print(f"Length vs Quality: Long tweets score {insights['length_vs_quality']['long_tweets_avg']} avg")
    
    print("\n🏆 Multi-Dimensional Rankings:")
    rankings = leaderboard.get_multi_dimensional_rankings()
    print(f"Total Rising Stars: {len(rankings['rising_stars'])}")
    print(f"Consistency Champions: {len(rankings['consistency_champions'])}")
