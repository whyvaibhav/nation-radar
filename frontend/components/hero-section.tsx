"use client"

import { useEffect, useState } from "react"
import { Users, Brain, ArrowUp, MessageSquare, BarChart3 } from "lucide-react"

interface HeroSectionProps {
  totalTweets: number
  averageScore: number
  contentAnalyzed: number
  activeUsers: number
}

export function HeroSection({ totalTweets, averageScore, contentAnalyzed, activeUsers }: HeroSectionProps) {
  const [animatedValues, setAnimatedValues] = useState({
    totalTweets: 0,
    averageScore: 0,
    contentAnalyzed: 0,
    activeUsers: 0,
  })

  useEffect(() => {
    const animateNumbers = () => {
      const duration = 2000
      const steps = 60
      const stepDuration = duration / steps

      let currentStep = 0
      const interval = setInterval(() => {
        currentStep++
        const progress = currentStep / steps
        const easeOutQuart = 1 - Math.pow(1 - progress, 4)

        setAnimatedValues({
          totalTweets: Math.floor(totalTweets * easeOutQuart),
          averageScore: averageScore * easeOutQuart,
          contentAnalyzed: Math.floor(contentAnalyzed * easeOutQuart),
          activeUsers: Math.floor(activeUsers * easeOutQuart),
        })

        if (currentStep >= steps) {
          clearInterval(interval)
          setAnimatedValues({ totalTweets, averageScore, contentAnalyzed, activeUsers })
        }
      }, stepDuration)

      return () => clearInterval(interval)
    }

    animateNumbers()
  }, [totalTweets, averageScore, contentAnalyzed, activeUsers])

  return (
    <section className="px-6 py-8 max-w-7xl mx-auto">
      <div className="text-center mb-8">
        <h2 className="text-5xl lg:text-6xl font-bold mb-4 leading-tight" style={{ color: "rgba(116, 122, 111, 0.9)" }}>
          Nation Network <span style={{ color: "#D0FF16" }}>Analytics</span>
        </h2>
        <p
          className="text-xl font-medium leading-relaxed max-w-2xl mx-auto"
          style={{ color: "rgba(116, 122, 111, 0.6)" }}
        >
          Real-time insights into community engagement and growth metrics
        </p>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="nation-card group hover:scale-105 transition-all duration-300 p-6">
          <div
            className="w-14 h-14 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:rotate-12 transition-transform duration-300"
            style={{ background: "rgba(208, 255, 22, 0.15)", border: "2px solid rgba(208, 255, 22, 0.3)" }}
          >
            <MessageSquare className="w-7 h-7" style={{ color: "#D0FF16" }} />
          </div>
          <div className="text-center">
            <span
              className="block text-base font-semibold mb-2 uppercase tracking-wider"
              style={{ color: "rgba(116, 122, 111, 0.8)" }}
            >
              Total Tweets
            </span>
            <span className="block text-4xl lg:text-5xl font-black mb-2" style={{ color: "#D0FF16" }}>
              {animatedValues.totalTweets.toLocaleString()}
            </span>
            <div className="flex items-center justify-center gap-1 text-base font-medium" style={{ color: "#D0FF16" }}>
              <ArrowUp className="w-5 h-5" />
              <span>+12.5%</span>
            </div>
          </div>
        </div>

        <div className="nation-card group hover:scale-105 transition-all duration-300 p-6">
          <div
            className="w-14 h-14 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:rotate-12 transition-transform duration-300"
            style={{ background: "rgba(208, 255, 22, 0.15)", border: "2px solid rgba(208, 255, 22, 0.3)" }}
          >
            <BarChart3 className="w-7 h-7" style={{ color: "#D0FF16" }} />
          </div>
          <div className="text-center">
            <span
              className="block text-base font-semibold mb-2 uppercase tracking-wider"
              style={{ color: "rgba(116, 122, 111, 0.8)" }}
            >
              Average Score
            </span>
            <span className="block text-4xl lg:text-5xl font-black mb-2" style={{ color: "#D0FF16" }}>
              {animatedValues.averageScore.toFixed(1)}/10
            </span>
            <div className="flex items-center justify-center gap-1 text-base font-medium" style={{ color: "#D0FF16" }}>
              <ArrowUp className="w-5 h-5" />
              <span>+0.3</span>
            </div>
          </div>
        </div>

        <div className="nation-card group hover:scale-105 transition-all duration-300 p-6">
          <div
            className="w-14 h-14 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:rotate-12 transition-transform duration-300"
            style={{ background: "rgba(208, 255, 22, 0.15)", border: "2px solid rgba(208, 255, 22, 0.3)" }}
          >
            <Brain className="w-7 h-7" style={{ color: "#D0FF16" }} />
          </div>
          <div className="text-center">
            <span
              className="block text-base font-semibold mb-2 uppercase tracking-wider"
              style={{ color: "rgba(116, 122, 111, 0.8)" }}
            >
              Content Analyzed
            </span>
            <span className="block text-4xl lg:text-5xl font-black mb-2" style={{ color: "#D0FF16" }}>
              {(animatedValues.contentAnalyzed / 1000000).toFixed(1)}M
            </span>
            <div className="flex items-center justify-center gap-1 text-base font-medium" style={{ color: "#D0FF16" }}>
              <ArrowUp className="w-5 h-5" />
              <span>+8.2%</span>
            </div>
          </div>
        </div>

        <div className="nation-card group hover:scale-105 transition-all duration-300 p-6">
          <div
            className="w-14 h-14 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:rotate-12 transition-transform duration-300"
            style={{ background: "rgba(208, 255, 22, 0.15)", border: "2px solid rgba(208, 255, 22, 0.3)" }}
          >
            <Users className="w-7 h-7" style={{ color: "#D0FF16" }} />
          </div>
          <div className="text-center">
            <span
              className="block text-base font-semibold mb-2 uppercase tracking-wider"
              style={{ color: "rgba(116, 122, 111, 0.8)" }}
            >
              Active Users
            </span>
            <span className="block text-4xl lg:text-5xl font-black mb-2" style={{ color: "#D0FF16" }}>
              {animatedValues.activeUsers.toLocaleString()}
            </span>
            <div className="flex items-center justify-center gap-1 text-base font-medium" style={{ color: "#D0FF16" }}>
              <ArrowUp className="w-5 h-5" />
              <span>+5.7%</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
