"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { TrendingUp, MessageSquare, BarChart3, Users } from "lucide-react"
import { useEffect, useState } from "react"

function useCountUp(end: number, duration = 2000) {
  const [count, setCount] = useState(0)

  useEffect(() => {
    let startTime: number
    let animationFrame: number

    const animate = (currentTime: number) => {
      if (!startTime) startTime = currentTime
      const progress = Math.min((currentTime - startTime) / duration, 1)

      setCount(Math.floor(progress * end))

      if (progress < 1) {
        animationFrame = requestAnimationFrame(animate)
      }
    }

    animationFrame = requestAnimationFrame(animate)
    return () => cancelAnimationFrame(animationFrame)
  }, [end, duration])

  return count
}

export function MetricsSection() {
  const metrics = [
    {
      title: "Total Tweets",
      value: "2,847,392",
      rawValue: 2847392,
      change: "+12.5%",
      icon: MessageSquare,
      trend: "up",
    },
    {
      title: "Average Score",
      value: "1.4/2.0",
      rawValue: 1.4,
      change: "+0.3",
      icon: BarChart3,
      trend: "up",
    },
    {
      title: "Content Analyzed",
      value: "1.2M",
      rawValue: 1200000,
      change: "+8.2%",
      icon: TrendingUp,
      trend: "up",
    },
    {
      title: "Active Users",
      value: "45,231",
      rawValue: 45231,
      change: "+5.7%",
      icon: Users,
      trend: "up",
    },
  ]

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6">
      {metrics.map((metric, index) => (
        <MetricCard key={index} metric={metric} index={index} />
      ))}
    </div>
  )
}

function MetricCard({ metric, index }: { metric: any; index: number }) {
  const [isHovered, setIsHovered] = useState(false)
  const [isVisible, setIsVisible] = useState(false)

  const animatedValue = useCountUp(
    metric.title === "Average Score"
      ? metric.rawValue
      : metric.rawValue > 1000000
        ? metric.rawValue / 1000000
        : metric.rawValue,
    2000 + index * 200,
  )

  useEffect(() => {
    const timer = setTimeout(() => setIsVisible(true), index * 150)
    return () => clearTimeout(timer)
  }, [index])

  const formatValue = (value: number) => {
    if (metric.title === "Average Score") {
      return `${value.toFixed(2)}/2.0`
    }
    if (metric.title === "Content Analyzed") {
      return `${(value).toFixed(1)}M`
    }
    if (metric.title === "Total Tweets") {
      return value.toLocaleString()
    }
    return value.toLocaleString()
  }

  return (
    <Card
      className={`bg-card border-border transition-all duration-500 hover:scale-105 hover:shadow-xl hover:shadow-primary/20 cursor-pointer transform ${
        isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
      } ${isHovered ? "border-primary/50" : ""}`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground transition-colors duration-300">
          {metric.title}
        </CardTitle>
        <metric.icon
          className={`h-4 w-4 text-primary transition-all duration-300 ${isHovered ? "scale-110 rotate-12" : ""}`}
        />
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold text-foreground transition-all duration-300">
          {formatValue(animatedValue)}
        </div>
        <p
          className={`text-xs text-primary flex items-center mt-1 transition-all duration-300 ${
            isHovered ? "translate-x-1" : ""
          }`}
        >
          <TrendingUp className={`w-3 h-3 mr-1 transition-transform duration-300 ${isHovered ? "scale-110" : ""}`} />
          {metric.change} from last month
        </p>
      </CardContent>
    </Card>
  )
}
