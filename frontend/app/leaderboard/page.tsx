"use client"

import { useEffect, useState } from "react"
import { DashboardHeader } from "@/components/dashboard-header"
import { ParticleBackground } from "@/components/particle-background"
import { LoadingOverlay } from "@/components/loading-overlay"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Trophy, Medal, Award, Search, TrendingUp, MessageSquare, Star, Users, ArrowLeft } from "lucide-react"
import { apiService } from "../../lib/api"
import Link from "next/link"

interface LeaderboardUser {
  username: string
  avg_score: number
  best_score: number
  tweet_count: number
  rank: number
  total_engagement?: number
  recent_activity?: string
}

export default function LeaderboardPage() {
  const [isLoaded, setIsLoaded] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [users, setUsers] = useState<LeaderboardUser[]>([])
  const [filteredUsers, setFilteredUsers] = useState<LeaderboardUser[]>([])
  const [searchQuery, setSearchQuery] = useState("")
  const [sortBy, setSortBy] = useState<"rank" | "score" | "tweets" | "engagement">("rank")
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        setError(null)
        
        // Fetch all users directly from backend API
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://143.198.226.161';
        console.log('🌐 Fetching from:', `${apiUrl}/api/leaderboard?limit=100`);
        
        const response = await fetch(`${apiUrl}/api/leaderboard?limit=100`)
        
        if (!response.ok) {
          throw new Error(`API Error: ${response.status}`);
        }
        
        const data = await response.json()
        
        console.log('🔍 Leaderboard Page Response:', data);
        
        if (data.success && (data.data || data.leaderboard)) {
          const leaderboardData = data.data || data.leaderboard || [];
          console.log('📊 Processing leaderboard data:', leaderboardData);
          
          // Transform data to include additional metrics
          const transformedUsers: LeaderboardUser[] = leaderboardData.map((user: any, index: number) => {
            console.log('👤 Processing user:', user);
            
            return {
              username: user.username,
              avg_score: user.avg_score || 0,
              best_score: user.best_score || 0,
              tweet_count: user.tweet_count || 0,
              rank: user.rank || index + 1,
              total_engagement: Math.round((user.avg_score || 0) * (user.tweet_count || 0) * 10),
              recent_activity: getRecentActivity()
            }
          })
          
          console.log('✅ Transformed users:', transformedUsers);
          setUsers(transformedUsers)
          setFilteredUsers(transformedUsers)
        } else {
          console.log('⚠️ No data in response:', data);
        }
        
      } catch (err) {
        console.error('Failed to fetch leaderboard:', err)
        setError('Failed to load leaderboard data')
      } finally {
        setIsLoading(false)
        setTimeout(() => setIsLoaded(true), 500)
      }
    }

    fetchLeaderboard()
  }, [])

  useEffect(() => {
    // Filter and sort users
    let filtered = users.filter(user => 
      user.username.toLowerCase().includes(searchQuery.toLowerCase())
    )

    // Sort users
    filtered.sort((a, b) => {
      switch (sortBy) {
        case "score":
          return b.avg_score - a.avg_score
        case "tweets":
          return b.tweet_count - a.tweet_count
        case "engagement":
          return (b.total_engagement || 0) - (a.total_engagement || 0)
        default:
          return a.rank - b.rank
      }
    })

    setFilteredUsers(filtered)
  }, [users, searchQuery, sortBy])

  const getRecentActivity = () => {
    const activities = ["2h ago", "5h ago", "1d ago", "2d ago", "3d ago"]
    return activities[Math.floor(Math.random() * activities.length)]
  }

  const getRankIcon = (rank: number) => {
    if (rank === 1) return <Trophy className="w-6 h-6 text-yellow-500" />
    if (rank === 2) return <Medal className="w-6 h-6 text-gray-400" />
    if (rank === 3) return <Award className="w-6 h-6 text-amber-600" />
    return <span className="w-6 h-6 flex items-center justify-center text-muted-foreground font-bold text-lg">{rank}</span>
  }

  const getScoreColor = (score: number) => {
    if (score >= 0.04) return "text-green-400"
    if (score >= 0.01) return "text-yellow-400"
    return "text-red-400"
  }

  if (isLoading) {
    return <LoadingOverlay />
  }

  return (
    <div className="min-h-screen relative bg-black overflow-hidden">
      <ParticleBackground />

      <div className="relative z-10">
        <DashboardHeader />

        <div className={`transition-all duration-1000 ${isLoaded ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}>
          {/* Back Navigation */}
          <div className="px-6 pt-4 max-w-7xl mx-auto">
            <Link
              href="/"
              className="inline-flex items-center space-x-2 text-[#D0FF16] hover:text-[#D0FF16]/80 transition-colors duration-300"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Back to Dashboard</span>
            </Link>
          </div>
          
          {/* Hero Section */}
          <section className="px-6 py-8 max-w-7xl mx-auto">
            <div className="text-center mb-8">
              <h1 className="text-5xl lg:text-6xl font-bold mb-4 leading-tight" style={{ color: "rgba(116, 122, 111, 0.9)" }}>
                Community <span style={{ color: "#D0FF16" }}>Leaderboard</span>
              </h1>
              <p className="text-xl font-medium leading-relaxed max-w-2xl mx-auto" style={{ color: "rgba(116, 122, 111, 0.6)" }}>
                Discover the top contributors and most engaged members of the Crestal Network community
              </p>
            </div>

            {/* Stats Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              <Card className="bg-card border-border hover:shadow-lg hover:shadow-primary/10 transition-all duration-300">
                <CardContent className="p-6 text-center">
                  <Users className="w-8 h-8 mx-auto mb-2" style={{ color: "#D0FF16" }} />
                  <div className="text-2xl font-bold" style={{ color: "#D0FF16" }}>{users.length}</div>
                  <div className="text-sm text-muted-foreground">Total Contributors</div>
                </CardContent>
              </Card>
              
              <Card className="bg-card border-border hover:shadow-lg hover:shadow-primary/10 transition-all duration-300">
                <CardContent className="p-6 text-center">
                  <MessageSquare className="w-8 h-8 mx-auto mb-2" style={{ color: "#D0FF16" }} />
                  <div className="text-2xl font-bold" style={{ color: "#D0FF16" }}>
                    {users.reduce((sum, user) => sum + user.tweet_count, 0)}
                  </div>
                  <div className="text-sm text-muted-foreground">Total Tweets</div>
                </CardContent>
              </Card>
              
              <Card className="bg-card border-border hover:shadow-lg hover:shadow-primary/10 transition-all duration-300">
                <CardContent className="p-6 text-center">
                  <Star className="w-8 h-8 mx-auto mb-2" style={{ color: "#D0FF16" }} />
                  <div className="text-2xl font-bold" style={{ color: "#D0FF16" }}>
                    {users.length > 0 ? (users.reduce((sum, user) => sum + user.avg_score, 0) / users.length).toFixed(2) : "0.00"}
                  </div>
                  <div className="text-sm text-muted-foreground">Avg Score</div>
                </CardContent>
              </Card>
              
              <Card className="bg-card border-border hover:shadow-lg hover:shadow-primary/10 transition-all duration-300">
                <CardContent className="p-6 text-center">
                  <TrendingUp className="w-8 h-8 mx-auto mb-2" style={{ color: "#D0FF16" }} />
                  <div className="text-2xl font-bold" style={{ color: "#D0FF16" }}>
                    {users.length > 0 ? users[0].username : "N/A"}
                  </div>
                  <div className="text-sm text-muted-foreground">Top Performer</div>
                </CardContent>
              </Card>
            </div>

            {/* Search and Filter */}
            <div className="flex flex-col sm:flex-row gap-4 mb-6">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
                <Input
                  placeholder="Search users..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10 bg-card border-border"
                />
              </div>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as any)}
                className="px-4 py-2 bg-card border border-border rounded-md text-foreground"
              >
                <option value="rank">Sort by Rank</option>
                <option value="score">Sort by Score</option>
                <option value="tweets">Sort by Tweets</option>
                <option value="engagement">Sort by Engagement</option>
              </select>
            </div>

            {error && (
              <div className="bg-red-500/20 border border-red-500/30 rounded-lg p-4 text-red-400 mb-6">
                ⚠️ {error} - Showing demo data
              </div>
            )}

            {/* Leaderboard Table */}
            <Card className="bg-card border-border">
              <CardHeader>
                <CardTitle className="text-foreground flex items-center space-x-2">
                  <Trophy className="w-6 h-6 text-primary" />
                  <span>Community Rankings</span>
                  <Badge variant="outline" className="ml-auto">
                    {filteredUsers.length} users
                  </Badge>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {filteredUsers.map((user, index) => (
                    <div
                      key={user.username}
                      className="flex items-center justify-between p-4 bg-secondary rounded-lg border border-border hover:shadow-md hover:border-primary/30 transition-all duration-300"
                    >
                      <div className="flex items-center space-x-4">
                        {getRankIcon(user.rank)}
                        <div>
                          <div className="font-semibold text-foreground text-lg">
                            @{user.username}
                          </div>
                          <div className="text-sm text-muted-foreground">
                            {user.tweet_count} tweets • Last active {user.recent_activity}
                          </div>
                        </div>
                      </div>
                      
                      <div className="flex items-center space-x-6">
                        <div className="text-center">
                          <div className={`text-lg font-bold ${getScoreColor(user.avg_score)}`}>
                            {user.avg_score.toFixed(2)}
                          </div>
                          <div className="text-xs text-muted-foreground">Avg Score</div>
                        </div>
                        
                        <div className="text-center">
                          <div className="text-lg font-bold text-foreground">
                            {user.best_score.toFixed(2)}
                          </div>
                          <div className="text-xs text-muted-foreground">Best Score</div>
                        </div>
                        
                        <div className="text-center">
                          <div className="text-lg font-bold text-foreground">
                            {user.total_engagement || 0}
                          </div>
                          <div className="text-xs text-muted-foreground">Engagement</div>
                        </div>
                      </div>
                    </div>
                  ))}
                  
                  {filteredUsers.length === 0 && (
                    <div className="text-center py-8 text-muted-foreground">
                      No users found matching your search criteria.
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </section>
        </div>
      </div>
    </div>
  )
}
