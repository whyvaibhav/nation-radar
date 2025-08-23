"use client"

import { useState, useEffect } from "react"
import { X, MessageSquare, Star, TrendingUp, Users, Calendar, Award } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

interface UserProfile {
  username: string
  stats: {
    total_tweets: number
    avg_score: number
    best_score: number
    total_engagement: number
    rank: string
  }
  tweets: Array<{
    id: string
    text: string
    score: number
    created_at: string
    engagement: {
      likes: number
      retweets: number
      replies: number
      views: number
      bookmarks: number
      quote_tweets: number
    }
  }>
  recent_activity: string
}

interface UserProfileModalProps {
  isOpen: boolean
  onClose: () => void
  username: string | null
}

export function UserProfileModal({ isOpen, onClose, username }: UserProfileModalProps) {
  const [profile, setProfile] = useState<UserProfile | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (isOpen && username) {
      fetchUserProfile(username)
    }
  }, [isOpen, username])

  const fetchUserProfile = async (username: string) => {
    try {
      setIsLoading(true)
      setError(null)
      
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://143.198.226.161'
      const response = await fetch(`${apiUrl}/api/user-profile/${username}`)
      
      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`)
      }
      
      const data = await response.json()
      
      if (data.success && data.data) {
        setProfile(data.data)
      } else {
        throw new Error(data.error || 'Failed to load profile')
      }
    } catch (err) {
      console.error('Failed to fetch user profile:', err)
      setError('Failed to load user profile')
    } finally {
      setIsLoading(false)
    }
  }

  const getScoreColor = (score: number) => {
    if (score >= 0.04) return "text-green-400"
    if (score >= 0.01) return "text-yellow-400"
    return "text-red-400"
  }

  const formatDate = (dateString: string) => {
    try {
      return new Date(dateString).toLocaleDateString()
    } catch {
      return 'Unknown date'
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-black border border-[rgba(208,255,22,0.2)] rounded-lg max-w-4xl w-full max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-[rgba(208,255,22,0.1)]">
          <div className="flex items-center space-x-3">
            <Users className="w-6 h-6" style={{ color: "#D0FF16" }} />
            <h2 className="text-2xl font-bold" style={{ color: "#D0FF16" }}>
              {username ? `@${username}` : 'User Profile'}
            </h2>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-[rgba(208,255,22,0.1)] rounded-lg transition-colors"
          >
            <X className="w-6 h-6" style={{ color: "#D0FF16" }} />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto max-h-[calc(90vh-120px)]">
          {isLoading && (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#D0FF16] mx-auto"></div>
              <p className="mt-2" style={{ color: "rgba(208,255,22,0.7)" }}>Loading profile...</p>
            </div>
          )}

          {error && (
            <div className="text-center py-8">
              <p className="text-red-400">{error}</p>
            </div>
          )}

          {profile && (
            <div className="space-y-6">
              {/* Stats Cards */}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <Card className="bg-card border-[rgba(208,255,22,0.1)]">
                  <CardContent className="p-4 text-center">
                    <MessageSquare className="w-6 h-6 mx-auto mb-2" style={{ color: "#D0FF16" }} />
                    <div className="text-2xl font-bold" style={{ color: "#D0FF16" }}>
                      {profile.stats.total_tweets}
                    </div>
                    <div className="text-sm text-muted-foreground">Total Tweets</div>
                  </CardContent>
                </Card>

                <Card className="bg-card border-[rgba(208,255,22,0.1)]">
                  <CardContent className="p-4 text-center">
                    <Star className="w-6 h-6 mx-auto mb-2" style={{ color: "#D0FF16" }} />
                    <div className="text-2xl font-bold" style={{ color: "#D0FF16" }}>
                      {profile.stats.avg_score.toFixed(2)}
                    </div>
                    <div className="text-sm text-muted-foreground">Avg Score</div>
                  </CardContent>
                </Card>

                <Card className="bg-card border-[rgba(208,255,22,0.1)]">
                  <CardContent className="p-4 text-center">
                    <Award className="w-6 h-6 mx-auto mb-2" style={{ color: "#D0FF16" }} />
                    <div className="text-2xl font-bold" style={{ color: "#D0FF16" }}>
                      {profile.stats.best_score.toFixed(2)}
                    </div>
                    <div className="text-sm text-muted-foreground">Best Score</div>
                  </CardContent>
                </Card>

                <Card className="bg-card border-[rgba(208,255,22,0.1)]">
                  <CardContent className="p-4 text-center">
                    <TrendingUp className="w-6 h-6 mx-auto mb-2" style={{ color: "#D0FF16" }} />
                    <div className="text-2xl font-bold" style={{ color: "#D0FF16" }}>
                      {profile.stats.total_engagement.toLocaleString()}
                    </div>
                    <div className="text-sm text-muted-foreground">Engagement</div>
                  </CardContent>
                </Card>
              </div>

              {/* Recent Activity */}
              <Card className="bg-card border-[rgba(208,255,22,0.1)]">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Calendar className="w-5 h-5" style={{ color: "#D0FF16" }} />
                    <span style={{ color: "#D0FF16" }}>Recent Activity</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground">{profile.recent_activity}</p>
                </CardContent>
              </Card>

              {/* Tweets List */}
              <Card className="bg-card border-[rgba(208,255,22,0.1)]">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <MessageSquare className="w-5 h-5" style={{ color: "#D0FF16" }} />
                    <span style={{ color: "#D0FF16" }}>Top Tweets</span>
                    <Badge variant="secondary" className="ml-2">
                      {profile.tweets.length} tweets
                    </Badge>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {profile.tweets.map((tweet, index) => (
                      <div
                        key={tweet.id}
                        className="p-4 border border-[rgba(208,255,22,0.1)] rounded-lg hover:border-[rgba(208,255,22,0.2)] transition-colors"
                      >
                        <div className="flex items-start justify-between mb-2">
                          <div className="flex items-center space-x-2">
                            <span className="text-sm text-muted-foreground">#{index + 1}</span>
                            <Badge 
                              className={getScoreColor(tweet.score)}
                              variant="outline"
                            >
                              Score: {tweet.score.toFixed(2)}
                            </Badge>
                          </div>
                          <span className="text-xs text-muted-foreground">
                            {formatDate(tweet.created_at)}
                          </span>
                        </div>
                        
                        <p className="text-sm mb-3 leading-relaxed">{tweet.text}</p>
                        
                        <div className="flex items-center space-x-4 text-xs text-muted-foreground">
                          <span>❤️ {tweet.engagement.likes}</span>
                          <span>🔄 {tweet.engagement.retweets}</span>
                          <span>💬 {tweet.engagement.replies}</span>
                          <span>👁️ {tweet.engagement.views}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
