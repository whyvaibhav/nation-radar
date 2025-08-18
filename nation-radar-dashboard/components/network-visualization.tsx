"use client"

import { useEffect, useRef } from "react"

export function NetworkVisualization() {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext("2d")
    if (!ctx) return

    canvas.width = canvas.offsetWidth
    canvas.height = 300

    const nodes = Array.from({ length: 20 }, () => ({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 2,
      vy: (Math.random() - 0.5) * 2,
      radius: Math.random() * 5 + 3,
      connections: Math.floor(Math.random() * 3) + 1,
    }))

    function animate() {
      if (!ctx || !canvas) return

      ctx.clearRect(0, 0, canvas.width, canvas.height)

      // Update node positions
      nodes.forEach((node) => {
        node.x += node.vx
        node.y += node.vy

        if (node.x < 0 || node.x > canvas.width) node.vx *= -1
        if (node.y < 0 || node.y > canvas.height) node.vy *= -1
      })

      // Draw connections
      ctx.strokeStyle = "rgba(208, 255, 22, 0.3)"
      ctx.lineWidth = 1
      nodes.forEach((node, i) => {
        nodes.slice(i + 1).forEach((otherNode) => {
          const distance = Math.sqrt(Math.pow(node.x - otherNode.x, 2) + Math.pow(node.y - otherNode.y, 2))
          if (distance < 100) {
            ctx.beginPath()
            ctx.moveTo(node.x, node.y)
            ctx.lineTo(otherNode.x, otherNode.y)
            ctx.stroke()
          }
        })
      })

      // Draw nodes
      nodes.forEach((node) => {
        ctx.beginPath()
        ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2)
        ctx.fillStyle = "#D0FF16"
        ctx.fill()

        // Add glow effect
        ctx.shadowColor = "#D0FF16"
        ctx.shadowBlur = 10
        ctx.fill()
        ctx.shadowBlur = 0
      })

      requestAnimationFrame(animate)
    }

    animate()

    const handleResize = () => {
      canvas.width = canvas.offsetWidth
      canvas.height = 300
    }

    window.addEventListener("resize", handleResize)
    return () => window.removeEventListener("resize", handleResize)
  }, [])

  return (
    <div className="nation-card p-6">
      <h3 className="text-xl font-bold text-nation-green mb-4 flex items-center gap-2">
        <span className="w-2 h-2 bg-nation-green rounded-full animate-pulse"></span>
        NETWORK ACTIVITY
      </h3>
      <canvas ref={canvasRef} className="w-full h-[300px] rounded-lg bg-black/50" />
      <div className="mt-4 grid grid-cols-3 gap-4 text-sm">
        <div className="text-center">
          <div className="text-nation-green font-bold">1,247</div>
          <div className="text-gray-400">Active Nodes</div>
        </div>
        <div className="text-center">
          <div className="text-nation-green font-bold">89.3%</div>
          <div className="text-gray-400">Network Health</div>
        </div>
        <div className="text-center">
          <div className="text-nation-green font-bold">2.4ms</div>
          <div className="text-gray-400">Avg Latency</div>
        </div>
      </div>
    </div>
  )
}
