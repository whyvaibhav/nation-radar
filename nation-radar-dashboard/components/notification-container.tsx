"use client"

import { useState, useEffect } from "react"
import { X, CheckCircle, AlertCircle, Info } from "lucide-react"

interface Notification {
  id: string
  message: string
  type: "success" | "error" | "warning" | "info"
  timestamp: Date
}

export function NotificationContainer() {
  const [notifications, setNotifications] = useState<Notification[]>([])

  useEffect(() => {
    // Add welcome notification
    const welcomeNotification: Notification = {
      id: "1",
      message: "🚀 Nation Radar Dashboard Loaded!",
      type: "success",
      timestamp: new Date(),
    }

    setNotifications([welcomeNotification])

    // Auto-remove after 5 seconds
    const timer = setTimeout(() => {
      setNotifications([])
    }, 5000)

    return () => clearTimeout(timer)
  }, [])

  const removeNotification = (id: string) => {
    setNotifications((prev) => prev.filter((n) => n.id !== id))
  }

  const getIcon = (type: string) => {
    switch (type) {
      case "success":
        return <CheckCircle className="w-5 h-5" />
      case "error":
        return <AlertCircle className="w-5 h-5" />
      case "warning":
        return <AlertCircle className="w-5 h-5" />
      default:
        return <Info className="w-5 h-5" />
    }
  }

  const getColorClass = (type: string) => {
    switch (type) {
      case "success":
        return "border-green-500/50 bg-green-500/10"
      case "error":
        return "border-red-500/50 bg-red-500/10"
      case "warning":
        return "border-yellow-500/50 bg-yellow-500/10"
      default:
        return "border-blue-500/50 bg-blue-500/10"
    }
  }

  return (
    <div className="fixed top-8 right-8 z-50 space-y-4">
      {notifications.map((notification) => (
        <div
          key={notification.id}
          className={`glass-effect p-4 max-w-sm border ${getColorClass(notification.type)} fade-in`}
        >
          <div className="flex items-start gap-3">
            <div className="text-white">{getIcon(notification.type)}</div>
            <div className="flex-1">
              <p className="text-white font-medium">{notification.message}</p>
            </div>
            <button
              onClick={() => removeNotification(notification.id)}
              className="text-white/60 hover:text-white transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>
      ))}
    </div>
  )
}
