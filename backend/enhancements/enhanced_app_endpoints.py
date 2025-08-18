# Add these endpoints to your app.py for Vercel

from quick_improvements import CrestalAnalytics, EnhancedLeaderboard

@app.route('/api/rising-stars', methods=['GET'])
def get_rising_stars():
    """Get users with rapidly improving scores"""
    try:
        analytics = CrestalAnalytics('groktweets.csv')
        rising_stars = analytics.get_rising_stars()
        
        return jsonify({
            'success': True,
            'rising_stars': rising_stars
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/user-trends/<username>', methods=['GET'])
def get_user_trends(username):
    """Get detailed user analysis"""
    try:
        analytics = CrestalAnalytics('groktweets.csv')
        trends = analytics.get_user_trends(username)
        achievements = analytics.get_achievements(username)
        
        if trends:
            trends['achievements'] = achievements
            return jsonify({
                'success': True,
                'user_data': trends
            })
        else:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/enhanced-leaderboards', methods=['GET'])
def get_enhanced_leaderboards():
    """Get multi-dimensional leaderboard rankings"""
    try:
        leaderboard = EnhancedLeaderboard('groktweets.csv')
        rankings = leaderboard.get_multi_dimensional_rankings()
        
        return jsonify({
            'success': True,
            'leaderboards': rankings
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/community-insights', methods=['GET'])
def get_community_insights():
    """Get community health and content insights"""
    try:
        analytics = CrestalAnalytics('groktweets.csv')
        insights = analytics.get_content_insights()
        
        return jsonify({
            'success': True,
            'insights': insights
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
