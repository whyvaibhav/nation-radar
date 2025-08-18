"use client"

import { useEffect, useState } from "react"
import { DashboardHeader } from "@/components/dashboard-header"
import { TrendingContent } from "@/components/trending-content"
import { Leaderboard } from "@/components/leaderboard"
import { ActivityFeed } from "@/components/activity-feed"
import { ParticleBackground } from "@/components/particle-background"
import { LoadingOverlay } from "@/components/loading-overlay"
import { HeroSection } from "@/components/hero-section"
import { CommandTerminal } from "@/components/command-terminal"
import { DataRain } from "@/components/data-rain"
import { LiveSocialFeed } from "@/components/live-social-feed"

export default function Dashboard() {
  const [isLoaded, setIsLoaded] = useState(false)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsLoading(false)
      setIsLoaded(true)
    }, 2000)

    return () => clearTimeout(timer)
  }, [])

  if (isLoading) {
    return <LoadingOverlay />
  }

  return (
    <div className="min-h-screen relative bg-black overflow-hidden">
      <ParticleBackground />
      <DataRain />

      <div className="relative z-10">
        <DashboardHeader />

        <div
          className={`transition-all duration-1000 ${isLoaded ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}
        >
          <HeroSection totalTweets={2847} averageScore={8.4} contentAnalyzed={1000000} activeUsers={45231} />
        </div>

        <main className="container mx-auto px-4 py-8 space-y-8 max-w-7xl">
          <div
            className={`grid grid-cols-1 xl:grid-cols-3 gap-8 transition-all duration-1000 delay-400 ${isLoaded ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}
          >
            <div className="xl:col-span-2 space-y-8">
              <TrendingContent />
              <LiveSocialFeed />
              <CommandTerminal />
              <ActivityFeed />
            </div>
            <div className="xl:col-span-1">
              <Leaderboard />
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}
