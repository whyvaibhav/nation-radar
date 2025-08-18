import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Trophy, TrendingUp, Users } from "lucide-react"

export function Leaderboard() {
  const topContributors = [
    {
      rank: 1,
      username: "@socialmedia_guru",
      score: 9.8,
      posts: 1247,
      engagement: "94.2%",
      change: "+2.1",
    },
    {
      rank: 2,
      username: "@content_creator",
      score: 9.6,
      posts: 892,
      engagement: "91.7%",
      change: "+1.8",
    },
    {
      rank: 3,
      username: "@digital_nomad",
      score: 9.4,
      posts: 756,
      engagement: "89.3%",
      change: "+0.9",
    },
    {
      rank: 4,
      username: "@tech_reviewer",
      score: 9.2,
      posts: 634,
      engagement: "87.1%",
      change: "+1.2",
    },
    {
      rank: 5,
      username: "@startup_life",
      score: 9.0,
      posts: 523,
      engagement: "85.6%",
      change: "+0.7",
    },
  ]

  const getRankIcon = (rank: number) => {
    if (rank === 1) return <Trophy className="w-5 h-5 text-yellow-500" />
    if (rank === 2) return <Trophy className="w-5 h-5 text-gray-400" />
    if (rank === 3) return <Trophy className="w-5 h-5 text-amber-600" />
    return <span className="w-5 h-5 flex items-center justify-center text-muted-foreground font-bold text-lg">{rank}</span>
  }

  return (
    <Card className="bg-card border-border">
      <CardHeader>
        <CardTitle className="text-foreground flex items-center space-x-2 text-xl">
          <Users className="w-6 h-6 text-primary" />
          <span>Top Contributors</span>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {topContributors.map((contributor) => (
          <div
            key={contributor.rank}
            className="flex items-center justify-between p-4 bg-secondary rounded-lg border border-border"
          >
            <div className="flex items-center space-x-3">
              {getRankIcon(contributor.rank)}
              <div>
                <p className="font-semibold text-primary text-lg">{contributor.username}</p>
                <div className="flex items-center space-x-2 text-base text-muted-foreground">
                  <span>{contributor.posts} posts</span>
                  <span>•</span>
                  <span>{contributor.engagement} engagement</span>
                </div>
              </div>
            </div>

            <div className="text-right">
              <div className="flex items-center space-x-1">
                <Badge variant="outline" className="text-primary border-primary text-base">
                  {contributor.score}
                </Badge>
              </div>
              <div className="flex items-center space-x-1 text-base text-green-400 mt-1">
                <TrendingUp className="w-4 h-4" />
                <span>{contributor.change}</span>
              </div>
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  )
}
