"use client"

import { useState, useEffect, useRef } from "react"

export function CommandTerminal() {
  const [logs, setLogs] = useState<string[]>([])
  const [currentLog, setCurrentLog] = useState("")
  const [isTyping, setIsTyping] = useState(false)
  const terminalRef = useRef<HTMLDivElement>(null)

  const systemLogs = [
    "🔍 Monitoring 47,832 social media accounts...",
    "📊 Processing sentiment analysis batch #1247",
    "⚡ Real-time data stream: 2.3k posts/min",
    "🎯 Detected trending hashtag: #NationRadar",
    "🔔 Alert: Brand mention spike detected (+340%)",
    "📈 Engagement rate increased by 23% in last hour",
    "🌍 Geographic analysis: Top activity in Asia-Pacific",
    "🤖 AI model accuracy: 94.7% sentiment classification",
    "⭐ Positive sentiment surge: +15% from yesterday",
    "🔐 Security scan complete: All systems secure",
  ]

  const statusUpdates = [
    "✅ Database connection: Optimal",
    "✅ API endpoints: All responsive",
    "✅ Data pipeline: Processing normally",
    "⚠️  High traffic detected: Scaling resources",
    "✅ Backup systems: Synchronized",
    "🔄 Cache refresh: Complete",
    "✅ Network latency: 12ms average",
    "📡 Data ingestion: 99.8% uptime",
  ]

  useEffect(() => {
    const interval = setInterval(() => {
      if (logs.length < 12) {
        const allLogs = [...systemLogs, ...statusUpdates]
        const randomLog = allLogs[Math.floor(Math.random() * allLogs.length)]
        const timestamp = new Date().toLocaleTimeString()

        setIsTyping(true)
        setCurrentLog(`[${timestamp}] ${randomLog}`)

        setTimeout(() => {
          setLogs((prev) => [...prev, `[${timestamp}] ${randomLog}`])
          setCurrentLog("")
          setIsTyping(false)
        }, 1500)
      } else {
        setLogs([])
      }
    }, 2500)

    return () => clearInterval(interval)
  }, [logs.length])

  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight
    }
  }, [logs])

  const getLogColor = (log: string) => {
    if (log.includes("✅")) return "text-green-400"
    if (log.includes("⚠️")) return "text-yellow-400"
    if (log.includes("🔔") || log.includes("📈")) return "text-nation-green"
    if (log.includes("🔍") || log.includes("📊")) return "text-blue-400"
    return "text-gray-300"
  }

  return (
    <div className="nation-card p-6">
      <div className="flex items-center gap-2 mb-4">
        <div className="w-3 h-3 rounded-full bg-red-500"></div>
        <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
        <div className="w-3 h-3 rounded-full bg-green-500"></div>
        <span className="text-nation-green text-sm font-semibold ml-2">NATION SYSTEM MONITOR</span>
        <div className="ml-auto flex items-center gap-2">
          <div className="w-2 h-2 bg-nation-green rounded-full animate-pulse"></div>
          <span className="text-xs text-gray-400">LIVE</span>
        </div>
      </div>

      <div ref={terminalRef} className="bg-black rounded-lg p-4 h-64 overflow-y-auto text-sm">
        {logs.map((log, index) => (
          <div key={index} className={`mb-1 ${getLogColor(log)}`}>
            {log}
          </div>
        ))}
        {isTyping && (
          <div className="text-nation-green">
            {currentLog}
            <span className="animate-pulse">|</span>
          </div>
        )}
      </div>
    </div>
  )
}
