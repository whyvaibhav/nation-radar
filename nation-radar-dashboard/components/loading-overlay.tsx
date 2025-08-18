import { Radar } from "lucide-react"

export function LoadingOverlay() {
  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-lg flex items-center justify-center z-50">
      <div className="glass-effect p-12 text-center max-w-md">
        <div className="relative mb-8">
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="w-20 h-20 border-2 border-[#adff2f] rounded-full animate-ping"></div>
          </div>
          <div className="relative z-10 w-20 h-20 bg-gradient-to-br from-[#adff2f] to-[#6366f1] rounded-full flex items-center justify-center mx-auto">
            <Radar className="w-10 h-10 text-white animate-spin" />
          </div>
        </div>
        <h3 className="text-2xl font-bold text-white mb-4">Analyzing Crestal Network...</h3>
        <p className="text-gray-200 mb-8">Gathering real-time intelligence data</p>
        <div className="w-full h-1 bg-white/20 rounded-full overflow-hidden">
          <div className="h-full bg-gradient-to-r from-[#adff2f] to-[#6366f1] rounded-full animate-pulse"></div>
        </div>
      </div>
    </div>
  )
}
