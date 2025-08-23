"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Heart, MessageCircle, Repeat2, Eye, TrendingUp, BarChart3, Users, Target } from "lucide-react"
import { useState, useEffect } from "react"
import { apiService } from "../lib/api"

export function EnhancedMetrics() {
  const [engagementMetrics, setEngagementMetrics] = useState<any>(null)
  const [qualityMetrics, setQualityMetrics] = useState<any>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const [engagement, quality] = await Promise.all([
          apiService.getEngagementMetrics(),
          apiService.getQualityDistribution()
        ])
        
        setEngagementMetrics(engagement.data)
        setQualityMetrics(quality.data)
      } catch (error) {
        console.error('Failed to fetch enhanced metrics:', error)
      } finally {
        setIsLoading(false)
      }
    }

    fetchMetrics()
  }, [])

  if (isLoading) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6">
        {[...Array(8)].map((_, i) => (
          <Card key={i} className="bg-card border-border animate-pulse">
            <CardHeader className="pb-2">
              <div className="h-4 bg-muted rounded w-3/4"></div>
            </CardHeader>
            <CardContent>
              <div className="h-8 bg-muted rounded w-1/2 mb-2"></div>
              <div className="h-3 bg-muted rounded w-1/3"></div>
            </CardContent>
          </Card>
        ))}
      </div>
    )
  }

  const metrics = [
    // Engagement Metrics
    {
      title: "Avg Likes",
      value: engagementMetrics?.avg_likes || 0,
      icon: Heart,
      color: "text-red-400",
      trend: "+5.2%"
    },
    {
      title: "Avg Retweets", 
      value: engagementMetrics?.avg_retweets || 0,
      icon: Repeat2,
      color: "text-blue-400",
      trend: "+2.1%"
    },
    {
      title: "Avg Replies",
      value: engagementMetrics?.avg_replies || 0,
      icon: MessageCircle,
      color: "text-green-400",
      trend: "+8.7%"
    },
    {
      title: "Avg Views",
      value: engagementMetrics?.avg_views || 0,
      icon: Eye,
      color: "text-purple-400",
      trend: "+12.3%"
    },
    // Quality Metrics
    {
      title: "High Quality",
      value: `${qualityMetrics?.high_percentage || 0}%`,
      subtitle: `${qualityMetrics?.high_quality || 0} tweets`,
      icon: TrendingUp,
      color: "text-green-400",
      trend: "+3.4%"
    },
    {
      title: "Medium Quality",
      value: `${qualityMetrics?.medium_percentage || 0}%`,
      subtitle: `${qualityMetrics?.medium_quality || 0} tweets`,
      icon: BarChart3,
      color: "text-yellow-400",
      trend: "-1.2%"
    },
    {
      title: "Low Quality",
      value: `${qualityMetrics?.low_percentage || 0}%`,
      subtitle: `${qualityMetrics?.low_quality || 0} tweets`,
      icon: Target,
      color: "text-red-400",
      trend: "-2.1%"
    },
    {
      title: "Engagement Rate",
      value: `${engagementMetrics?.engagement_rate || 0}%`,
      subtitle: `${engagementMetrics?.total_engagement || 0} total`,
      icon: Users,
      color: "text-blue-400",
      trend: "+6.8%"
    }
  ]

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h3 className="text-2xl font-bold text-foreground mb-2">Enhanced Analytics</h3>
        <p className="text-muted-foreground">Detailed engagement and quality metrics</p>
      </div>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6">
        {metrics.map((metric, index) => (
          <Card key={index} className="bg-card border-border hover:shadow-lg hover:shadow-primary/10 transition-all duration-300">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                {metric.title}
              </CardTitle>
              <metric.icon className={`h-4 w-4 ${metric.color}`} />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-foreground">
                {metric.value}
              </div>
              {metric.subtitle && (
                <p className="text-xs text-muted-foreground mt-1">
                  {metric.subtitle}
                </p>
              )}
              <div className="flex items-center text-xs text-primary mt-2">
                <TrendingUp className="w-3 h-3 mr-1" />
                {metric.trend}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
