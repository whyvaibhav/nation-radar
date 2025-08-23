"use client"

import { useEffect, useState } from "react"
import { DashboardHeader } from "@/components/dashboard-header"
import { TrendingContent } from "@/components/trending-content"
import { Leaderboard } from "@/components/leaderboard"
import { ActivityFeed } from "@/components/activity-feed"
import { ParticleBackground } from "@/components/particle-background"

import { HeroSection } from "@/components/hero-section"

import { DataRain } from "@/components/data-rain"
import { EnhancedMetrics } from "@/components/enhanced-metrics"

import { apiService, Tweet, SystemStats } from "../lib/api"

export default function Dashboard() {
  const [isLoaded, setIsLoaded] = useState(true)
  const [isLoading, setIsLoading] = useState(false)
  const [tweets, setTweets] = useState<Tweet[]>([])
  const [leaderboard, setLeaderboard] = useState<Tweet[]>([])
  const [stats, setStats] = useState<SystemStats>({
    total_tweets: 0,
    recent_tweets_24h: 0,
    average_score: 0,
    top_score: 0,
    last_updated: ''
  })
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setError(null)
        
        // Fetch data from API
        const [tweetsResponse, leaderboardResponse, statsResponse] = await Promise.all([
          apiService.getTweets(100),  // Increased from 50 to 100
          apiService.getLeaderboard(20),
          apiService.getSystemStats()
        ])

        setTweets(tweetsResponse.data || [])
        setLeaderboard(leaderboardResponse.data || [])
        setStats(statsResponse.statistics)
        
      } catch (err) {
        console.error('Failed to fetch data:', err)
        setError('Failed to load data from backend')
      }
    }

    // Fetch data immediately
    fetchData()

    // No loading timer - instant load
    setIsLoading(false)
    setIsLoaded(true)

    // Set up auto-refresh every 30 seconds for real-time updates
    const refreshInterval = setInterval(() => {
      console.log('🔄 Auto-refreshing data...')
      fetchData()
    }, 30000) // 30 seconds

    return () => {
      clearInterval(refreshInterval)
    }
  }, [])



  return (
    <div className="min-h-screen relative bg-black overflow-hidden">
      <ParticleBackground />
      <DataRain />

      <div className="relative z-10">
        <DashboardHeader />

        <div
          className={`transition-all duration-1000 ${isLoaded ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}
        >
          <HeroSection 
            totalTweets={stats.total_tweets} 
            averageScore={stats.average_score} 
            contentAnalyzed={stats.total_tweets} 
            activeUsers={stats.recent_tweets_24h} 
          />
        </div>

        {error && (
          <div className="container mx-auto px-4 py-4">
            <div className="bg-red-500/20 border border-red-500/30 rounded-lg p-4 text-red-400">
              ⚠️ {error} - Showing demo data
            </div>
          </div>
        )}

        <main className="container mx-auto px-4 py-8 space-y-8 max-w-7xl">
          {/* Enhanced Metrics Section */}
          <div
            className={`transition-all duration-1000 delay-200 ${isLoaded ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}
          >
            <EnhancedMetrics />
          </div>
          
          <div
            className={`grid grid-cols-1 xl:grid-cols-3 gap-8 transition-all duration-1000 delay-400 ${isLoaded ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}
          >
            <div className="xl:col-span-2 space-y-8">
              <TrendingContent tweets={tweets} />
              <ActivityFeed tweets={tweets.slice(0, 15)} />
            </div>
            <div className="xl:col-span-1">
              <Leaderboard tweets={leaderboard} />
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}
