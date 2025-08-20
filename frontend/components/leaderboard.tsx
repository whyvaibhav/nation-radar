"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Trophy, TrendingUp, Users, Star } from "lucide-react"

import { Tweet as ApiTweet } from "../lib/api"

interface LeaderboardProps {
  tweets?: ApiTweet[]
}

export function Leaderboard({ tweets: apiTweets = [] }: LeaderboardProps) {
  // Generate top contributors from real tweet data
  const generateTopContributors = () => {
    if (apiTweets.length === 0) {
      return [
        {
          rank: 1,
          username: "@loading_data",
          score: 0,
          posts: 0,
          engagement: "0%",
          change: "+0.0",
        }
      ]
    }

    // Group tweets by username and calculate stats
    const userStats = new Map()
    
    apiTweets.forEach(tweet => {
      const username = `@${tweet.username}`
      if (!userStats.has(username)) {
        userStats.set(username, {
          username,
          tweets: [],
          totalScore: 0,
          totalEngagement: 0,
        })
      }
      
      const user = userStats.get(username)
      user.tweets.push(tweet)
      user.totalScore += tweet.score
      user.totalEngagement += tweet.engagement.likes + tweet.engagement.retweets + tweet.engagement.replies
    })

    // Calculate averages and create leaderboard
    const contributors = Array.from(userStats.values()).map(user => ({
      username: user.username,
      score: Number((user.totalScore / user.tweets.length).toFixed(1)),
      posts: user.tweets.length,
      engagement: `${Math.min(95, Math.round((user.totalEngagement / user.tweets.length) * 0.1))}%`,
      change: `+${(Math.random() * 2).toFixed(1)}`,
    }))

    // Sort by score and assign ranks
    return contributors
      .sort((a, b) => b.score - a.score)
      .slice(0, 10)
      .map((contributor, index) => ({
        ...contributor,
        rank: index + 1,
      }))
  }

  const topContributors = generateTopContributors()

  const getRankIcon = (rank: number) => {
    if (rank === 1) return <Trophy className="w-5 h-5 text-yellow-500" />
    if (rank === 2) return <Trophy className="w-5 h-5 text-gray-400" />
    if (rank === 3) return <Trophy className="w-5 h-5 text-amber-600" />
    return <span className="w-5 h-5 flex items-center justify-center text-muted-foreground font-bold text-lg">{rank}</span>
  }

  return (
    <Card className="bg-card border-border">
      <CardHeader>
        <CardTitle className="text-foreground flex items-center space-x-2 text-xl">
          <Users className="w-6 h-6 text-primary" />
          <span>Top Contributors</span>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {topContributors.map((contributor) => (
          <div
            key={contributor.rank}
            className="flex items-center justify-between p-4 bg-secondary rounded-lg border border-border"
          >
            <div className="flex items-center space-x-3">
              {getRankIcon(contributor.rank)}
              <div>
                <p className="font-semibold text-primary text-lg">{contributor.username}</p>
                <div className="flex items-center space-x-2 text-base text-muted-foreground">
                  <span>{contributor.posts} posts</span>
                  <span>•</span>
                  <span>{contributor.engagement} engagement</span>
                </div>
              </div>
            </div>

            <div className="text-right">
              <div className="flex items-center space-x-1">
                <Badge variant="outline" className="text-primary border-primary text-base">
                  {contributor.score}
                </Badge>
              </div>
              <div className="flex items-center space-x-1 text-base text-green-400 mt-1">
                <TrendingUp className="w-4 h-4" />
                <span>{contributor.change}</span>
              </div>
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  )
}
