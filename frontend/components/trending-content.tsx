"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Heart, MessageCircle, Repeat2, Share, TrendingUp } from "lucide-react"
import { useState, useEffect } from "react"

export function TrendingContent() {
  const [visibleTweets, setVisibleTweets] = useState<number[]>([])
  const [hoveredTweet, setHoveredTweet] = useState<number | null>(null)

  const trendingTweets = [
    {
      id: 1,
      author: "@techinfluencer",
      content:
        "The future of AI is here and it's transforming how we interact with technology. Exciting times ahead! 🚀",
      score: 9.2,
      likes: 1247,
      retweets: 342,
      replies: 89,
      timestamp: "2h ago",
      sentiment: "positive",
    },
    {
      id: 2,
      author: "@cryptoexpert",
      content:
        "Market analysis shows interesting patterns emerging. The next few weeks will be crucial for the industry.",
      score: 8.7,
      likes: 892,
      retweets: 156,
      replies: 67,
      timestamp: "4h ago",
      sentiment: "neutral",
    },
    {
      id: 3,
      author: "@startupfounder",
      content: "Just closed our Series A! Grateful for the amazing team and investors who believed in our vision. 💪",
      score: 9.5,
      likes: 2341,
      retweets: 567,
      replies: 123,
      timestamp: "6h ago",
      sentiment: "positive",
    },
  ]

  useEffect(() => {
    trendingTweets.forEach((tweet, index) => {
      setTimeout(() => {
        setVisibleTweets((prev) => [...prev, tweet.id])
      }, index * 200)
    })
  }, [])

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
            } ${hoveredTweet === tweet.id ? "bg-secondary/80" : ""}`}
            onMouseEnter={() => setHoveredTweet(tweet.id)}
            onMouseLeave={() => setHoveredTweet(null)}
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
                  className={`text-sm transition-all duration-300 ${getSentimentColor(tweet.sentiment)} ${
                    hoveredTweet === tweet.id ? "scale-105" : ""
                  }`}
                >
                  {tweet.sentiment}
                </Badge>
                <Badge
                  variant="outline"
                  className={`text-primary border-primary transition-all duration-300 text-sm ${
                    hoveredTweet === tweet.id ? "scale-105 bg-primary/10" : ""
                  }`}
                >
                  Score: {tweet.score}
                </Badge>
              </div>
            </div>

            <p className="text-foreground mb-4 transition-colors duration-300 text-base leading-relaxed">{tweet.content}</p>

            <div className="flex items-center justify-between text-muted-foreground">
              <div className="flex items-center space-x-6">
                <div
                  className={`flex items-center space-x-2 transition-all duration-300 hover:text-red-400 cursor-pointer ${
                    hoveredTweet === tweet.id ? "scale-110" : ""
                  }`}
                >
                  <Heart className="w-5 h-5 hover:fill-current" />
                  <span className="text-base">{tweet.likes.toLocaleString()}</span>
                </div>
                <div
                  className={`flex items-center space-x-2 transition-all duration-300 hover:text-blue-400 cursor-pointer ${
                    hoveredTweet === tweet.id ? "scale-110" : ""
                  }`}
                >
                  <Repeat2 className="w-5 h-5" />
                  <span className="text-base">{tweet.retweets}</span>
                </div>
                <div
                  className={`flex items-center space-x-2 transition-all duration-300 hover:text-primary cursor-pointer ${
                    hoveredTweet === tweet.id ? "scale-110" : ""
                  }`}
                >
                  <MessageCircle className="w-5 h-5" />
                  <span className="text-base">{tweet.replies}</span>
                </div>
              </div>
              <Share
                className={`w-5 h-5 cursor-pointer hover:text-primary transition-all duration-300 ${
                  hoveredTweet === tweet.id ? "scale-110 rotate-12" : ""
                }`}
              />
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  )
}
