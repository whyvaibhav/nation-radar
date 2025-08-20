"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Heart, MessageCircle, Repeat2, Share, TrendingUp } from "lucide-react"
import { useState, useEffect } from "react"
import { Tweet } from "../lib/api"

interface TrendingContentProps {
  tweets: Tweet[]
}

export function TrendingContent({ tweets }: TrendingContentProps) {
  const [visibleTweets, setVisibleTweets] = useState<(string | number)[]>([])

  // Helper functions defined first
  const formatTime = (timestamp: string) => {
    try {
      const date = new Date(timestamp)
      const now = new Date()
      const diffMs = now.getTime() - date.getTime()
      const diffMins = Math.floor(diffMs / 60000)
      const diffHours = Math.floor(diffMs / 3600000)
      const diffDays = Math.floor(diffMs / 86400000)
      
      if (diffMins < 1) return 'Just now'
      if (diffMins < 60) return `${diffMins}m ago`
      if (diffHours < 24) return `${diffHours}h ago`
      if (diffDays < 7) return `${diffDays}d ago`
      
      return date.toLocaleDateString()
    } catch {
      return 'Unknown'
    }
  }

  const getSentimentFromScore = (score: number) => {
    if (score >= 1.5) return "positive"
    if (score <= 0.5) return "negative"
    return "neutral"
  }

  // Use real tweets if available, otherwise show demo data
  const trendingTweets = tweets.length > 0 ? tweets.slice(0, 5).map((tweet, index) => ({
    id: tweet.id,
    author: `@${tweet.username}`,
    content: tweet.text.length > 100 ? tweet.text.substring(0, 100) + '...' : tweet.text,
    score: tweet.score,
    likes: tweet.engagement.likes,
    retweets: tweet.engagement.retweets,
    replies: tweet.engagement.replies,
    timestamp: formatTime(tweet.created_at),
    sentiment: getSentimentFromScore(tweet.score),
  })) : [
    {
      id: 1,
      author: "@techinfluencer",
      content: "Loading real data from Nation Radar backend...",
      score: 0,
      likes: 0,
      retweets: 0,
      replies: 0,
      timestamp: "Loading...",
      sentiment: "neutral",
    }
  ]

  useEffect(() => {
    trendingTweets.forEach((tweet, index) => {
      setTimeout(() => {
        setVisibleTweets((prev) => [...prev, tweet.id])
      }, index * 200)
    })
  }, [trendingTweets])

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case "positive":
        return "bg-green-500/20 text-green-400 border-green-500/30"
      case "negative":
        return "bg-red-500/20 text-red-400 border-red-500/30"
      default:
        return "bg-yellow-500/20 text-yellow-400 border-yellow-500/30"
    }
  }



  return (
    <Card className="bg-card border-border hover:shadow-lg hover:shadow-primary/10 transition-all duration-300">
      <CardHeader>
        <CardTitle className="text-foreground flex items-center space-x-2 text-xl">
          <TrendingUp className="w-6 h-6 text-primary animate-pulse" />
          <span>Trending Content</span>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {trendingTweets.map((tweet, index) => (
          <div
            key={tweet.id}
            className={`p-5 bg-secondary rounded-lg border border-border transition-all duration-500 hover:scale-[1.02] hover:shadow-md hover:border-primary/30 cursor-pointer transform ${
              visibleTweets.includes(tweet.id) ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"
            }`}
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center space-x-3">
                <span className="font-semibold text-primary transition-colors duration-300 hover:text-primary/80 text-lg">
                  {tweet.author}
                </span>
                <span className="text-muted-foreground text-base">{tweet.timestamp}</span>
              </div>
              <div className="flex items-center space-x-3">
                <Badge
                  className={`text-sm transition-all duration-300 ${getSentimentColor(tweet.sentiment)}`}
                >
                  {tweet.sentiment}
                </Badge>
                <Badge className="bg-primary/20 text-primary border-primary/30">
                  Score: {tweet.score.toFixed(2)}
                </Badge>
              </div>
            </div>
            
            <p className="text-foreground mb-4 leading-relaxed">{tweet.content}</p>
            
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4 text-muted-foreground">
                <div className="flex items-center space-x-1">
                  <Heart className="w-4 h-4" />
                  <span className="text-sm">{tweet.likes}</span>
                </div>
                <div className="flex items-center space-x-1">
                  <Repeat2 className="w-4 h-4" />
                  <span className="text-sm">{tweet.retweets}</span>
                </div>
                <div className="flex items-center space-x-1">
                  <MessageCircle className="w-4 h-4" />
                  <span className="text-sm">{tweet.replies}</span>
                </div>
              </div>
              
              <div className="flex items-center space-x-2">
                <Share className="w-4 h-4 text-muted-foreground hover:text-primary transition-colors cursor-pointer" />
              </div>
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  )
}
