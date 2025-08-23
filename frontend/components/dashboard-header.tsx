import { Search, Trophy } from "lucide-react"
import Image from "next/image"
import Link from "next/link"

export function DashboardHeader() {
  return (
    <header className="nation-header">
      <div className="header-content">
        <div className="brand-section">
          <div className="relative">
            <Image src="/images/nation-icon.png" alt="Nation Logo" width={72} height={72} className="nation-logo" />
          </div>
        </div>

        <div className="flex flex-col items-center mx-1 flex-1">
          <Image
            src="/images/nation-title.png"
            alt="Nation Radar"
            width={300}
            height={60}
            className="nation-logo mb-2"
          />
          <div className="connection-status">
            <div className="status-indicator">
              <div className="status-dot"></div>
              <span className="status-text text-lg">Live Monitoring</span>
            </div>
          </div>
        </div>

        <div className="header-actions">
          <div className="flex items-center space-x-4">
            <Link
              href="/leaderboard"
              className="flex items-center space-x-2 px-4 py-2 bg-transparent border border-[rgba(208,255,22,0.12)] rounded-lg text-[#D0FF16] hover:border-[rgba(208,255,22,0.25)] hover:bg-[rgba(208,255,22,0.05)] transition-all duration-300"
            >
              <Trophy className="w-4 h-4" />
              <span className="hidden sm:inline">Leaderboard</span>
            </Link>
            
            <div className="relative hidden md:block">
              <Search
                className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5"
                style={{ color: "rgba(208, 255, 22, 0.6)" }}
              />
              <input
                placeholder="Search content..."
                className="pl-10 pr-4 py-3 w-72 bg-transparent border border-[rgba(208,255,22,0.12)] rounded-lg text-[#D0FF16] placeholder:text-[rgba(208,255,22,0.4)] focus:border-[rgba(208,255,22,0.25)] focus:outline-none transition-all duration-300 hover:border-[rgba(208,255,22,0.2)] focus:shadow-[0_0_20px_rgba(208,255,22,0.1)] text-base"
              />
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}
