"use client"

import { useState, useEffect } from "react"
import { Heart, MessageCircle, Repeat2, Share } from "lucide-react"

interface Tweet {
  id: string
  username: string
  handle: string
  content: string
  timestamp: string
  likes: number
  retweets: number
  replies: number
  sentiment: "positive" | "negative" | "neutral"
}

export function LiveSocialFeed() {
  const [tweets, setTweets] = useState<Tweet[]>([])
  const [typingTweet, setTypingTweet] = useState<Tweet | null>(null)
  const [typedContent, setTypedContent] = useState("")

  const mockTweets: Tweet[] = [
    {
      id: "1",
      username: "TechEnthusiast",
      handle: "@techie_2024",
      content:
        "Just discovered Nation Radar - this social monitoring tool is incredible! The real-time analytics are game-changing 🚀",
      timestamp: "2m",
      likes: 47,
      retweets: 12,
      replies: 8,
      sentiment: "positive",
    },
    {
      id: "2",
      username: "DataScientist",
      handle: "@data_guru",
      content:
        "Nation's sentiment analysis accuracy is impressive. Finally, a tool that understands context and nuance in social conversations.",
      timestamp: "5m",
      likes: 23,
      retweets: 6,
      replies: 3,
      sentiment: "positive",
    },
    {
      id: "3",
      username: "MarketingPro",
      handle: "@marketing_maven",
      content:
        "The dashboard visualization in Nation Radar makes complex social data so easy to understand. Perfect for client presentations!",
      timestamp: "8m",
      likes: 31,
      retweets: 9,
      replies: 5,
      sentiment: "positive",
    },
    {
      id: "4",
      username: "SocialMediaMgr",
      handle: "@social_expert",
      content:
        "Nation Radar's real-time monitoring caught a potential PR issue before it escalated. Saved our brand reputation!",
      timestamp: "12m",
      likes: 89,
      retweets: 34,
      replies: 15,
      sentiment: "positive",
    },
  ]

  const typeText = (text: string, callback: () => void) => {
    let index = 0
    setTypedContent("")

    const interval = setInterval(() => {
      if (index < text.length) {
        setTypedContent(text.slice(0, index + 1))
        index++
      } else {
        clearInterval(interval)
        setTimeout(callback, 1000)
      }
    }, 50)
  }

  useEffect(() => {
    const addNewTweet = () => {
      const randomTweet = mockTweets[Math.floor(Math.random() * mockTweets.length)]
      const newTweet = {
        ...randomTweet,
        id: Date.now().toString(),
        timestamp: "now",
      }

      setTypingTweet(newTweet)
      typeText(newTweet.content, () => {
        setTweets((prev) => [newTweet, ...prev.slice(0, 4)])
        setTypingTweet(null)
        setTypedContent("")
      })
    }

    const interval = setInterval(addNewTweet, 8000)
    addNewTweet() // Initial tweet

    return () => clearInterval(interval)
  }, [])

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case "positive":
        return "text-green-400"
      case "negative":
        return "text-red-400"
      default:
        return "text-gray-400"
    }
  }

  return (
    <div className="nation-card p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold text-nation-green">Live Social Feed</h3>
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 bg-nation-green rounded-full animate-pulse"></div>
          <span className="text-sm text-gray-400">LIVE</span>
        </div>
      </div>

      <div className="space-y-4 max-h-96 overflow-y-auto">
        {typingTweet && (
          <div className="border border-nation-green/20 rounded-lg p-4 bg-nation-green/5">
            <div className="flex items-start gap-3">
              <div className="w-10 h-10 bg-nation-green/20 rounded-full flex items-center justify-center">
                <span className="text-nation-green font-bold text-sm">{typingTweet.username[0]}</span>
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-2">
                  <span className="font-semibold text-white">{typingTweet.username}</span>
                  <span className="text-gray-400 text-sm">{typingTweet.handle}</span>
                  <span className="text-gray-500 text-sm">• {typingTweet.timestamp}</span>
                </div>
                <p className="text-gray-300">
                  {typedContent}
                  <span className="animate-pulse">|</span>
                </p>
              </div>
            </div>
          </div>
        )}

        {tweets.map((tweet) => (
          <div
            key={tweet.id}
            className="border border-gray-700 rounded-lg p-4 hover:border-nation-green/30 transition-colors"
          >
            <div className="flex items-start gap-3">
              <div className="w-10 h-10 bg-gray-700 rounded-full flex items-center justify-center">
                <span className="text-nation-green font-bold text-sm">{tweet.username[0]}</span>
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-2">
                  <span className="font-semibold text-white">{tweet.username}</span>
                  <span className="text-gray-400 text-sm">{tweet.handle}</span>
                  <span className="text-gray-500 text-sm">• {tweet.timestamp}</span>
                  <span className={`text-xs px-2 py-1 rounded ${getSentimentColor(tweet.sentiment)}`}>
                    {tweet.sentiment}
                  </span>
                </div>
                <p className="text-gray-300 mb-3">{tweet.content}</p>
                <div className="flex items-center gap-6 text-gray-500">
                  <button className="flex items-center gap-1 hover:text-nation-green transition-colors">
                    <MessageCircle size={16} />
                    <span className="text-sm">{tweet.replies}</span>
                  </button>
                  <button className="flex items-center gap-1 hover:text-nation-green transition-colors">
                    <Repeat2 size={16} />
                    <span className="text-sm">{tweet.retweets}</span>
                  </button>
                  <button className="flex items-center gap-1 hover:text-nation-green transition-colors">
                    <Heart size={16} />
                    <span className="text-sm">{tweet.likes}</span>
                  </button>
                  <button className="hover:text-nation-green transition-colors">
                    <Share size={16} />
                  </button>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
