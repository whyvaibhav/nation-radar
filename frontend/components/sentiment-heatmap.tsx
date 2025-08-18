"use client"

import { useState, useEffect } from "react"

interface RegionData {
  name: string
  sentiment: number
  volume: number
  trend: "up" | "down" | "stable"
}

export function SentimentHeatmap() {
  const [regions, setRegions] = useState<RegionData[]>([
    { name: "North America", sentiment: 0.78, volume: 15420, trend: "up" },
    { name: "Europe", sentiment: 0.65, volume: 12890, trend: "stable" },
    { name: "Asia Pacific", sentiment: 0.82, volume: 18750, trend: "up" },
    { name: "Latin America", sentiment: 0.71, volume: 8340, trend: "down" },
    { name: "Middle East", sentiment: 0.59, volume: 5670, trend: "stable" },
    { name: "Africa", sentiment: 0.73, volume: 6890, trend: "up" },
  ])

  const [globalSentiment, setGlobalSentiment] = useState(0.72)

  useEffect(() => {
    const interval = setInterval(() => {
      setRegions((prev) =>
        prev.map((region) => ({
          ...region,
          sentiment: Math.max(0, Math.min(1, region.sentiment + (Math.random() - 0.5) * 0.1)),
          volume: Math.max(1000, region.volume + Math.floor((Math.random() - 0.5) * 1000)),
          trend: Math.random() > 0.7 ? (Math.random() > 0.5 ? "up" : "down") : region.trend,
        })),
      )

      setGlobalSentiment((prev) => Math.max(0, Math.min(1, prev + (Math.random() - 0.5) * 0.05)))
    }, 5000)

    return () => clearInterval(interval)
  }, [])

  const getSentimentColor = (sentiment: number) => {
    if (sentiment >= 0.8) return "bg-green-500"
    if (sentiment >= 0.6) return "bg-yellow-500"
    return "bg-red-500"
  }

  const getSentimentIntensity = (sentiment: number) => {
    return Math.floor(sentiment * 100)
  }

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case "up":
        return "↗"
      case "down":
        return "↘"
      default:
        return "→"
    }
  }

  const getTrendColor = (trend: string) => {
    switch (trend) {
      case "up":
        return "text-green-400"
      case "down":
        return "text-red-400"
      default:
        return "text-gray-400"
    }
  }

  return (
    <div className="nation-card p-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-xl font-bold text-nation-green">Global Sentiment Analysis</h3>
        <div className="flex items-center gap-2">
          <span className="text-sm text-gray-400">Global Score:</span>
          <span className="text-2xl font-bold text-nation-green">{Math.floor(globalSentiment * 100)}%</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
        {regions.map((region) => (
          <div
            key={region.name}
            className="bg-gray-800/50 rounded-lg p-4 border border-gray-700 hover:border-nation-green/30 transition-all"
          >
            <div className="flex items-center justify-between mb-3">
              <h4 className="font-semibold text-white">{region.name}</h4>
              <span className={`text-lg ${getTrendColor(region.trend)}`}>{getTrendIcon(region.trend)}</span>
            </div>

            <div className="flex items-center gap-3 mb-2">
              <div className="flex-1 bg-gray-700 rounded-full h-2">
                <div
                  className={`h-2 rounded-full transition-all duration-1000 ${getSentimentColor(region.sentiment)}`}
                  style={{ width: `${getSentimentIntensity(region.sentiment)}%` }}
                ></div>
              </div>
              <span className="text-sm font-bold text-white">{getSentimentIntensity(region.sentiment)}%</span>
            </div>

            <div className="flex justify-between text-sm text-gray-400">
              <span>Volume: {region.volume.toLocaleString()}</span>
              <span className={getSentimentColor(region.sentiment).replace("bg-", "text-")}>
                {region.sentiment >= 0.7 ? "Positive" : region.sentiment >= 0.5 ? "Neutral" : "Negative"}
              </span>
            </div>
          </div>
        ))}
      </div>

      <div className="bg-gray-800/30 rounded-lg p-4 border border-gray-700">
        <h4 className="font-semibold text-nation-green mb-3">Sentiment Distribution</h4>
        <div className="flex gap-4">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-green-500 rounded"></div>
            <span className="text-sm text-gray-300">Positive (70%)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-yellow-500 rounded"></div>
            <span className="text-sm text-gray-300">Neutral (20%)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-red-500 rounded"></div>
            <span className="text-sm text-gray-300">Negative (10%)</span>
          </div>
        </div>
      </div>
    </div>
  )
}
