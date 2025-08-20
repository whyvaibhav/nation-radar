"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Activity, MessageSquare, TrendingUp, AlertTriangle, CheckCircle } from "lucide-react"
import { useState, useEffect } from "react"

import { Tweet as ApiTweet } from "../app/api"

interface ActivityFeedProps {
  tweets?: ApiTweet[]
}

export function ActivityFeed({ tweets: apiTweets = [] }: ActivityFeedProps) {
  const [visibleActivities, setVisibleActivities] = useState<number[]>([])
  const [newActivity, setNewActivity] = useState(false)

  // Generate essential activities from real tweet data
  const generateActivities = () => {
    if (apiTweets.length === 0) {
      return [
        {
          id: 1,
          type: "loading",
          title: "Loading Real Data",
          description: "Connecting to Crestal Network backend...",
          timestamp: "now",
          status: "info",
          icon: Activity,
        }
      ]
    }

    const activities = []
    
    // Analysis summary
    const avgScore = (apiTweets.reduce((sum, t) => sum + t.score, 0) / apiTweets.length).toFixed(2)
    activities.push({
      id: 1,
      type: "analysis",
      title: "Data Analysis Complete",
      description: `Processed ${apiTweets.length} tweets • Average quality score: ${avgScore}`,
      timestamp: "2 minutes ago",
      status: "success",
      icon: CheckCircle,
    })

    // Top content alert
    const topTweet = apiTweets.reduce((max, tweet) => tweet.score > max.score ? tweet : max, apiTweets[0])
    activities.push({
      id: 2,
      type: "trending",
      title: "High-Quality Content Alert",
      description: `@${topTweet.username} posted exceptional content (Score: ${topTweet.score.toFixed(2)})`,
      timestamp: "15 minutes ago",
      status: "info",
      icon: TrendingUp,
    })

    // Sentiment overview
    const positiveCount = apiTweets.filter(t => t.score >= 1.5).length
    const percentage = Math.round((positiveCount / apiTweets.length) * 100)
    
    activities.push({
      id: 3,
      type: "alert",
      title: "Community Sentiment",
      description: `${percentage}% positive sentiment • Community engagement is ${percentage > 70 ? 'excellent' : percentage > 40 ? 'good' : 'moderate'}`,
      timestamp: "32 minutes ago",
      status: percentage > 70 ? "success" : percentage > 40 ? "info" : "warning",
      icon: AlertTriangle,
    })

    return activities
  }

  const activities = generateActivities()

  useEffect(() => {
    // Reset visible activities when tweets change
    setVisibleActivities([])
    
    activities.forEach((activity, index) => {
      setTimeout(() => {
        setVisibleActivities((prev) => [...prev, activity.id])
      }, index * 150)
    })

    // Simulate new activity every 10 seconds
    const interval = setInterval(() => {
      setNewActivity(true)
      setTimeout(() => setNewActivity(false), 2000)
    }, 10000)

    return () => clearInterval(interval)
  }, [apiTweets])

  const getStatusColor = (status: string) => {
    switch (status) {
      case "success":
        return "bg-green-500/20 text-green-400 border-green-500/30"
      case "warning":
        return "bg-yellow-500/20 text-yellow-400 border-yellow-500/30"
      case "error":
        return "bg-red-500/20 text-red-400 border-red-500/30"
      default:
        return "bg-blue-500/20 text-blue-400 border-blue-500/30"
    }
  }

  const getIconColor = (status: string) => {
    switch (status) {
      case "success":
        return "text-green-400"
      case "warning":
        return "text-yellow-400"
      case "error":
        return "text-red-400"
      default:
        return "text-blue-400"
    }
  }

  return (
    <Card className="bg-card border-border hover:shadow-lg hover:shadow-primary/10 transition-all duration-300">
      <CardHeader>
        <CardTitle className="text-foreground flex items-center space-x-2 text-xl">
          <Activity
            className={`w-6 h-6 text-primary transition-all duration-300 ${newActivity ? "animate-spin" : ""}`}
          />
          <span>Real-time Activity</span>
          {newActivity && <div className="w-3 h-3 bg-primary rounded-full animate-pulse"></div>}
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4 max-h-96 overflow-y-auto scrollbar-thin scrollbar-thumb-primary/20 scrollbar-track-transparent">
        {activities.map((activity, index) => (
          <div
            key={activity.id}
            className={`flex items-start space-x-4 p-4 bg-secondary rounded-lg border border-border transition-all duration-500 hover:scale-[1.02] hover:shadow-sm hover:border-primary/30 cursor-pointer transform ${
              visibleActivities.includes(activity.id) ? "opacity-100 translate-x-0" : "opacity-0 -translate-x-4"
            } ${index === 0 && newActivity ? "animate-pulse border-primary/50" : ""}`}
          >
            <div
              className={`p-3 rounded-full bg-secondary transition-all duration-300 hover:scale-110 ${getIconColor(activity.status)}`}
            >
              <activity.icon className="w-5 h-5" />
            </div>

            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between mb-2">
                <h4 className="font-semibold text-foreground transition-colors duration-300 hover:text-primary text-lg">
                  {activity.title}
                </h4>
                <Badge
                  className={`text-sm transition-all duration-300 hover:scale-105 ${getStatusColor(activity.status)}`}
                >
                  {activity.status}
                </Badge>
              </div>
              <p className="text-base text-muted-foreground mb-2 transition-colors duration-300 leading-relaxed">
                {activity.description}
              </p>
              <span className="text-sm text-muted-foreground">{activity.timestamp}</span>
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  )
}
